from flask import Flask, render_template, request, jsonify
import requests
import logging
import os, sys

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import common.fabai_common_variables


#code to get static text file and returns as stub for testing purposes
from common.fabai_get_static_debug_data import *

#for UI troubleshooting.  Return static response as if you called fabric ai
DEBUG_STATIC_FABRIC_RESPONSE = common.fabai_common_variables.DEBUG_STATIC_FABRIC_RESPONSE_VALUE

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

#location for static content when in debug mode to avoid hitting AI server
DEBUG_STATIC_FABRIC_FILE = os.path.join(current_directory, '..', 'static', 'fabai_fabric_static_response_to_webui_for_test.txt')

# Allow toggle on/off debugging from IDE
DEBUG_CODE = common.fabai_common_variables.DEBUG_CODE_VALUE
if DEBUG_CODE:
    DEBUG_PORT = common.fabai_common_variables.DEBUG_PORT_AIWEBUI_VALUE
    import debugpy
    # Listen for the VS Code debugger to attach on port 5678
    debugpy.listen(("0.0.0.0", DEBUG_PORT))
    print("Waiting for debugger to attach...")
    debugpy.wait_for_client()  # Pause execution until the debugger is attached

# Port number to run UI on
AIWEBUI_PORT_NUMBER = 5005

app = Flask(__name__)

# Get the current directory
current_directory = os.path.dirname(os.path.abspath(__file__))

# Set the log path to go up one directory and then to the log folder
LOG_PATH = os.path.join(current_directory, 'fabai_webui.log')

# Setup logging to log to a file
logging.basicConfig(
    filename=os.path.expanduser(LOG_PATH),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# URL for the new api_fabricAI service
FABRIC_AI_API_URL = "http://localhost:5006/get_ai_insights"

@app.route('/')
def index():
    app.logger.info(f"rendering index.html")
    return render_template('index.html')


def validate_request(function, operationtype, url, text_input):
    errors = []

    # Validate text input if function is "textInput"
    if function == 'textInput':
        if not text_input.strip():
            errors.append("Text input is required when 'Text Input' is selected.")

    # Validate URL input if function is "aiweb" or "aivideo"
    elif function in ['aiweb', 'aivideo']:
        if not url or not url.strip():
            errors.append("URL is required when 'AIWeb' or 'AIVideo' is selected.")

    # Return the list of errors if validation fails, or None if validation passes
    if errors:
        return errors

    return None 


@app.route('/submit', methods=['POST'])
def submit():
    
    app.logger.info(f"starting submit")
    # Get form data
    data = request.json
    function = data.get('function')
    operationtype = data.get('operationtype', 'wisdom')
    url = data.get('url')
    text_input = data.get('textInput',"")

    app.logger.info(f"DEBUG_CODE_VALUE={common.fabai_common_variables.DEBUG_CODE_VALUE}, DEBUG_STATIC_FABRIC_RESPONSE_VALUE={common.fabai_common_variables.DEBUG_STATIC_FABRIC_RESPONSE_VALUE}, DEBUG_STATIC_YOUTUBE_RESPONSE_VALUE={common.fabai_common_variables.DEBUG_STATIC_YOUTUBE_RESPONSE_VALUE}")
    app.logger.info(f"Received data: function={function}, operationtype={operationtype}, url={url}, text_input={text_input}")

    try:
        if DEBUG_STATIC_FABRIC_RESPONSE:
            output_data = get_static_debug_data(DEBUG_STATIC_FABRIC_FILE)
            app.logger.info(f"Using Fabric Static data {DEBUG_STATIC_FABRIC_FILE}")
        else:

            # Validate the request
            validation_errors = validate_request(function, operationtype, url, text_input)

            # If validation fails, return the error response
            if validation_errors:
                app.logger.info(f"Stopping user.  Failed validation.")
                return jsonify({'error': 'Validation failed', 'messages': validation_errors}), 400
            
            payload = {
                'function': function,
                'operationtype': operationtype,
                'url': url,
                'text_input': text_input
            }

            app.logger.info(f"Sending payload to API: {payload}")    
            
            response = requests.post(FABRIC_AI_API_URL, json=payload)
            response.raise_for_status()
            
            data = response.json()
            output_data = data.get('output', 'No output received.')
            app.logger.info(f"API response: {output_data}")

        return jsonify({"output": output_data})  # Return output as JSON

    except requests.exceptions.RequestException as e:
        app.logger.error(f"Error connecting to API: {e}")
        return jsonify({"error": f"Error connecting to API: {e}"}), 500  # Return JSON error response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=AIWEBUI_PORT_NUMBER)
