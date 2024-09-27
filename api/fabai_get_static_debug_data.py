import logging
from flask import Flask, request, jsonify
from fabai_common import *

app = Flask(__name__)

# Setup logging using the built-in logging module
logging.basicConfig(level=logging.INFO)

# Example static debug function
def get_static_debug_data():
    app.logger.info(f"get_static_debug_data - DEBUG_STATIC_FILE: {DEBUG_STATIC_FILE}")
    try:
        # Load the response from a plain text file
        with open(DEBUG_STATIC_FILE, 'r') as file:
            response = file.read()  # Read file as plain text
        return response
        
    except FileNotFoundError:
        raise GetStaticContentError("error: Stub file not found")
    except Exception as e:
        app.logger.error(f"Error reading the stub file: {e}")
        raise GetStaticContentError("error: Error reading the stub file")

#add entry point that can be called via CURL to test in isolation
@app.route('/test_get_static_debug_data', methods=['POST'])
def test_get_static_debug_data():
    return get_static_debug_data()

#if __name__ == '__main__':
#    app.run(debug=True, host='0.0.0.0', port=PORT_NUMBER)
