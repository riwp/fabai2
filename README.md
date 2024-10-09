

FabAI2

-----------------------
Progressive Web App
-----------------------

- extends fabai to make into a progressive web app that can be installed on phone
- adds support for https
- adds entry point for content to be posted directly to PWA
- Testing integration with iphone still in progress PWA works, still some things to work out with safari share to PWA
- Have not tested android

You will need to create your own certs or comment out in app load:
- You will need to generate your own certs and then install on ios (Replace $ variables with values)
- command to generate certs:  openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout "$KEY_FILE" -out "$CERT_FILE" -subj "/CN=$IP_ADDRESS" -addext "subjectAltName=DNS:$HostName,IP:$IP_ADDRESS"
- copy certificate.crt and private.key to aiwebui root directory
On IOS:
- share private.key with your ios app
- install by clicking on .cer (i used SMB samba share), VPN device Management, click on cert, install
- Then general, about, certificate trust settings, enable trust of certificate

For Progressive Web APP install (PWA)
- open aiwebui using https://[server]:5005
- use arrow to share, add home screen
- you should see icon as an app now on home screen that opens up

-----------------------
Python: Add browse, retrieve, delete
-----------------------

Key Features of the Back-End Code:

	1.	List Files (/files):
	•	Retrieves the list of files from the BASE_DIR directory.
	•	For each file, it fetches the corresponding description from the file_metadata.json file, or displays a default “No description available” message if no description is found.
	2.	Get File Content and Description (/files/<filename>):
	•	Fetches the content of a specific file and its description from the file_metadata.json file.
	•	If the file doesn’t exist, it returns a 404 error.
	3.	Add/Update File Description (/files/<filename>/description):
	•	Allows users to add or update a description for a specific file by sending a POST request.
	•	The description is stored in the file_metadata.json file.
	•	If the file doesn’t exist in the directory, it returns a 404 error.
	4.	Delete File (/files/<filename>):
	•	Deletes the specified file from the filesystem.
	•	Also removes the file’s metadata (description) from the file_metadata.json file.
	•	If the file doesn’t exist, it returns a 404 error.

Directory Structure:

Make sure you update the BASE_DIR to point to the directory where your files are stored. The file_metadata.json file will be created in the same directory as the Flask app unless you specify a different location.

Example of file_metadata.json File:

{
    "example.txt": {
        "description": "This is an example file."
    },
    "notes.txt": {
        "description": "Personal notes on project progress."
    }
}




import os
import json
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

# Define the directory where your files are stored and the JSON file for metadata
BASE_DIR = '/path/to/your/files/'  # Update this with your actual file directory
JSON_FILE = 'file_metadata.json'

# Helper function to load the metadata from the JSON file
def load_metadata():
    if not os.path.exists(JSON_FILE):
        return {}
    with open(JSON_FILE, 'r') as f:
        return json.load(f)

# Helper function to save the metadata to the JSON file
def save_metadata(metadata):
    with open(JSON_FILE, 'w') as f:
        json.dump(metadata, f, indent=4)

# Fetch file description from the metadata
def get_file_description(filename):
    metadata = load_metadata()
    return metadata.get(filename, {}).get('description', None)

# Update or add a description to the metadata
def update_file_description(filename, description):
    metadata = load_metadata()
    metadata[filename] = {'description': description}
    save_metadata(metadata)

# List all files in the directory along with their descriptions
@app.route('/files', methods=['GET'])
def list_files():
    files = [f for f in os.listdir(BASE_DIR) if os.path.isfile(os.path.join(BASE_DIR, f))]
    file_list = []
    
    for file in files:
        description = get_file_description(file)
        file_list.append({
            'filename': file,
            'description': description if description else "No description available"
        })
    
    return jsonify(file_list)

# Get file content and description for a specific file
@app.route('/files/<filename>', methods=['GET'])
def get_file_content(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.isfile(file_path):
        abort(404, "File not found")

    # Read file content
    with open(file_path, 'r') as file:
        content = file.read()

    # Get file description from JSON metadata
    description = get_file_description(filename)

    return jsonify({
        'content': content,
        'description': description
    })

# Add or update file description
@app.route('/files/<filename>/description', methods=['POST'])
def add_description(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.isfile(file_path):
        abort(404, "File not found")
    
    # Get the description from the request body
    data = request.get_json()
    description = data.get('description')

    if not description:
        abort(400, "Description is required")
    
    # Update the file description in the JSON metadata file
    update_file_description(filename, description)
    
    return jsonify({"message": "Description added/updated successfully"}), 200

# Delete a file and remove its metadata
@app.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(BASE_DIR, filename)
    if not os.path.isfile(file_path):
        abort(404, "File not found")

    # Remove the file from the filesystem
    os.remove(file_path)
    
    # Optionally remove file description from the metadata JSON
    metadata = load_metadata()
    if filename in metadata:
        del metadata[filename]
        save_metadata(metadata)

    return jsonify({"message": "File deleted successfully"}), 200

if __name__ == '__main__':
    # Initialize Flask app
    app.run(debug=True)


-----------------------
Web UI: Add browse, retrieve, delete
-----------------------

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>File Browser</title>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .file-list {
            margin-bottom: 20px;
        }
        .file-item {
            margin-bottom: 10px;
        }
        .description {
            font-style: italic;
            color: gray;
        }
        .file-content {
            white-space: pre-wrap;
            background-color: #f5f5f5;
            padding: 10px;
            border: 1px solid #ccc;
            margin-top: 10px;
        }
        .file-actions {
            margin-top: 10px;
        }
        button {
            margin-right: 5px;
        }
    </style>
</head>
<body>
    <h1>File Browser</h1>

    <div class="file-list">
        <h2>Files</h2>
        <div id="file-list-container"></div>
    </div>

    <div id="file-details" style="display: none;">
        <h2>File: <span id="file-name"></span></h2>
        <p id="file-description" class="description"></p>

        <textarea id="file-content" class="file-content" rows="10" cols="80" readonly></textarea>

        <div class="file-actions">
            <h3>Update Description:</h3>
            <input type="text" id="new-description" placeholder="Enter new description" />
            <button id="save-description">Save Description</button>
            <button id="delete-file">Delete File</button>
        </div>
    </div>

    <script>
        $(document).ready(function() {
            // Load file list on page load
            loadFileList();

            function loadFileList() {
                $.get("/files", function(data) {
                    $('#file-list-container').empty();
                    data.forEach(function(file) {
                        $('#file-list-container').append(
                            '<div class="file-item">' +
                            '<a href="#" class="file-link" data-filename="' + file.filename + '">' + file.filename + '</a>' +
                            ' <span class="description">(' + file.description + ')</span>' +
                            '</div>'
                        );
                    });

                    // Attach click handlers to file links
                    $('.file-link').click(function(e) {
                        e.preventDefault();
                        let filename = $(this).data('filename');
                        loadFileDetails(filename);
                    });
                });
            }

            function loadFileDetails(filename) {
                $('#file-details').show();
                $('#file-name').text(filename);
                $('#file-content').val('');

                // Get file description and content
                $.get("/files/" + filename, function(data) {
                    $('#file-content').val(data.content);
                    $('#file-description').text(data.description ? data.description : "No description available");
                });

                // Save description button click
                $('#save-description').off('click').on('click', function() {
                    let newDescription = $('#new-description').val();
                    if (newDescription) {
                        $.ajax({
                            url: "/files/" + filename + "/description",
                            type: "POST",
                            contentType: "application/json",
                            data: JSON.stringify({ description: newDescription }),
                            success: function() {
                                alert("Description updated");
                                loadFileList();  // Refresh the file list to show updated description
                                $('#file-description').text(newDescription);
                                $('#new-description').val('');  // Clear input field
                            },
                            error: function() {
                                alert("Error updating description");
                            }
                        });
                    } else {
                        alert("Please enter a description");
                    }
                });

                // Delete file button click
                $('#delete-file').off('click').on('click', function() {
                    if (confirm("Are you sure you want to delete this file?")) {
                        $.ajax({
                            url: "/files/" + filename,
                            type: "DELETE",
                            success: function() {
                                alert("File deleted");
                                loadFileList();
                                $('#file-details').hide();  // Hide details after deleting the file
                            },
                            error: function() {
                                alert("Error deleting file");
                            }
                        });
                    }
                });
            }
        });
    </script>
</body>
</html>