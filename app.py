import numpy as np
from flask import Flask, request, make_response
import json
import pickle
import logging
from logging.handlers import RotatingFileHandler
from flask_cors import cross_origin
from indic_transliteration import xsanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate
from df_response_lib import *

app = Flask(__name__)
#model = pickle.load(open('rf.pkl', 'rb'))

@app.route('/')
def hello():
    print('this is logging appplication')
    return 'Hello World'

@app.route('/webhook', methods=['POST'])
@cross_origin()
def webhook():

    req = request.get_json(silent=True, force=True)

    #print("Request:")
    #print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def processRequest(req):
	
    result = req.get("queryResult")

    #app.logger.info('logged in successfully')
    print(result)

    intent = result.get("intent").get('displayName')
    action = result.get('action')
	
	#log.write_log(sessionID, "Bot Says: "+intent)
    
    if (intent=='translate'):
	   	text = result.get("parameters").get("text")
	   	returntext=transliterate(text, xsanscript.ITRANS, xsanscript.KANNADA)
	   
	   	
	   	fulfillmentText= returntext
	   	return {
            "fulfillmentText": fulfillmentText
        }
    
    if (intent=='imageresponse'):
    	if action == 'getimage':
            fulfillmentText = 'Suggestion chips Response from webhook'
            print("inside image")
            aog = actions_on_google_response()
            aog_sr = aog.simple_response([
            [fulfillmentText, fulfillmentText, False]
            ])
            
            #log.write_log(sessionID, aog_sc = aog.suggestion_chips(["suggestion1", "suggestion2"])
            aog_sc = aog.suggestion_chips(["suggestion1", "suggestion2"])
            ff_response = fulfillment_response()
            ff_text = ff_response.fulfillment_text(fulfillmentText)
            ff_messages = ff_response.fulfillment_messages([aog_sr, aog_sc])
            reply = ff_response.main_response(ff_text, ff_messages)
                
    #user_says=result.get("queryText")
    #log.write_log(sessionID, "User Says: "+user_says)
    return reply
	       
if __name__ == '__main__':
    app.run()
#if __name__ == '__main__':
#    port = int(os.getenv('PORT', 5000))
#    print("Starting app on port %d" % port)
#    app.run(debug=False, port=port, host='0.0.0.0')
