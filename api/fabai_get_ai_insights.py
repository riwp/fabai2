import logging
from flask import Flask, request, jsonify

#import common variables, classes
from fabai_common import *

#code to get static text file and returns as stub for testing purposes
from fabai_get_static_debug_data import *

#code to download and clean up html and return clean text
from fabai_get_webpage_as_text import *

#code to get youtube transcripts
from fabai_get_youtubevideo_transcript import *

#code to call fabric and get insights
from fabai_get_fabric_insights_from_text import *


app = Flask(__name__)

# Setup logging using the built-in logging module
logging.basicConfig(level=logging.INFO)

#primary entry point into application called by web ui
@app.route('/get_ai_insights', methods=['POST'])
def get_AI_Insights():
    data = request.json
    
    #used to determine whether to get web or video or other source content
    function = data.get('function', 'aivideo')
    
    #contains the different fabric patterns to be mapped from web ui to parameters
    operation_type = data.get('operationtype')
    
    #the target url to get the content
    url = data.get('url')
    
    #when true, returns static content. when false downloads data from internet
    DEBUGGING = data.get('debug', False)
    
    app.logger.info(f"Received request: function={function}, operation_type={operation_type}, url={url}, DEBUGGING={DEBUGGING}")

    #If Debugging is on, return static content   
    if DEBUGGING:
        app.logger.info(f"Returning static data")
        return jsonify({"output": get_static_debug_data()})
        
    #if content type is video, get the youtube transcript and then pass it to fabric
    if function == 'aivideo':
        app.logger.info(f"calling get_youtubevideo_transcript with URL: {url}")
        youtube_transcript = get_youtubevideo_transcript(url)
        fabric_response = get_fabric_insights_from_text(function, operation_type, os.path.basename(url), youtube_transcript)
        
        #return json
        return jsonify({"output": fabric_response})

    #if content type is web, get the web html, clean it up, and then pass it to fabric
    elif function == 'aiweb':
        app.logger.info(f"calling get_webpage_as_text with URL: {url}")
        web_text = get_webpage_as_text(url)
        fabric_response = get_fabric_insights_from_text(function, operation_type, os.path.basename(url), web_text)
        
        #return json
        return jsonify({"output": fabric_response})
    #otherwise, not a valid type
    else:
        return jsonify({"error": "Invalid function. Supported values: 'aiweb', 'aivideo'."}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=API_PORT_NUMBER)
