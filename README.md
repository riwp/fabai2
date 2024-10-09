

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
Add browse, retrieve, delete
-----------------------

# Capabilities:

	1.	File List: When the /files endpoint is called, the list of files in the directory is retrieved. For each file, its description (if any) is fetched from the JSON metadata file and displayed in the response.
	2.	Add/Update Descriptions: The /files/<filename>/description endpoint allows users to add or update descriptions. The description is stored in the file_metadata.json file with the filename as the key.
	3.	JSON Storage: The descriptions are stored in a simple JSON file (file_metadata.json). If a file already has a description, it will be updated; otherwise, a new description is added.
	4.	Graceful Error Handling: The app handles missing files (returning a 404 if a file doesn’t exist) and missing descriptions (400 if the user tries to submit without providing a description).

# Main application

import os
import json
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

BASE_DIR = '/path/to/your/files/'
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

# List files along with their descriptions
@app.route('/files')
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

# Add or update file description
@app.route('/files/<filename>/description', methods=['POST'])
def add_description(filename):
    if not os.path.isfile(os.path.join(BASE_DIR, filename)):
        abort(404, "File not found")
    
    # Get the description from the request
    data = request.get_json()
    description = data.get('description')
    
    if not description:
        abort(400, "Description is required")
    
    # Update the file description in the JSON metadata file
    update_file_description(filename, description)
    
    return jsonify({"message": "Description added/updated successfully"}), 200

if __name__ == '__main__':
    app.run()


