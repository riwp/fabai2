import logging
import os  # Ensure os is imported
import subprocess
from flask import Flask, request, jsonify
from api.fabai_common import *  # Importing custom modules or configurations

app = Flask(__name__)

# Setup logging using the built-in logging module
logging.basicConfig(level=logging.INFO)

#calls fabric for insights
def get_fabric_insights_from_text(function, operation_type, base_filename, text_content):

    app.logger.info(f"Received request: operation_type={operation_type}, text_content={text_content}")

    if not operation_type or not text_content:
        raise GetInsightsError("error: operation_type and text_content are required")
    
    # Validate operation type and get corresponding fabric pattern
    if operation_type not in operation_mapping:
        raise GetInsightsError({"error": f"Invalid operationtype. Supported types: {', '.join(operation_mapping.keys())}"})

    #map the short pattern name to the actual parameter
    fabric_pattern = operation_mapping[operation_type]
    app.logger.info(f"Using fabric pattern: {fabric_pattern}")

    #make sure there is content and log for debugging purposes
    transcript_length = len(text_content)
    app.logger.info(f"Transcript length: {transcript_length} characters")

    #handle error when no content recieved
    if transcript_length == 0:
        app.logger.error("No subtitles received.")
        raise GetInsightsError("error: No subtitles received")

    #app.logger.info(f"Subtitles content: {text_content[:500]}...")  # Log first 500 characters of the subtitle

    # Prepare output filename
    filename_without_extension = os.path.splitext(base_filename)[0]

    #store the file name    
    output_file_name = ""
    
    #add video to the name if video
    if function == 'aivideo':
        output_file_name = os.path.join(OUTPUT_DIR_VIDEO, f"video_{operation_type}_{filename_without_extension}.txt")

    #add web to the name if video
    elif function == 'aiweb':  # Change `function` to `function`
        output_file_name = os.path.join(OUTPUT_DIR_WEB, f"video_{operation_type}_{filename_without_extension}.txt")
    
    #add web to the name if video
    elif function == 'textInput':  
        output_file_name = os.path.join(OUTPUT_DIR_TEXT, f"text_{operation_type}_{filename_without_extension}.txt")

    else:
        return jsonify({"error": f"invalid function {function}"}), 500
   
    # Prepare fabric command
    fabric_command = [
        "fabric", "--pattern", fabric_pattern
    ]

    # Log the command being executed
    app.logger.info(f"Executing command: {' '.join(fabric_command)}")

    try:
        # Run fabric command and capture stdout and stderr
        result = subprocess.run(fabric_command, input=text_content, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode != 0:
            error_message = result.stderr.strip()
            app.logger.error(f"Fabric command failed: {error_message}")
            raise GetInsightsError({"error": f"Fabric command failed: {error_message}"})

        # Write the output to the file
        with open(output_file_name, 'w') as output_file:
            output_file.write(result.stdout)
    except Exception as e:
        app.logger.error(f"Error running fabric command: {e}")
        raise GetInsightsError({"error": "Error executing fabric command"})  # Fix the syntax error here

    # Check if the output file contains data
    if os.path.getsize(output_file_name) == 0:
        app.logger.error("Fabric command completed but the output file is empty.")
        raise GetInsightsError("error: Output file is empty")

    # Read and return the contents of the output file
    try:
        with open(output_file_name, 'r') as output_file:
            output_content = output_file.read()
    except Exception as e:
        app.logger.error(f"Error reading output file: {e}")
        raise GetInsightsError("error: Error reading output file")

    app.logger.info(f"Output content: {output_content[:500]}...")  # Log first 500 characters of the output

    return output_content

#add entry point that can be called via CURL to test in isolation
@app.route('/test_get_webpage_as_text', methods=['POST'])
def test_get_fabric_insights_from_text():
    operation_type = request.json.get('operation_type')
    text_content = request.json.get('text_content')
    return get_fabric_insights_from_text(operation_type, text_content)

#if __name__ == '__main__':
#    app.run(host='0.0.0.0', port=PORT_NUMBER)
