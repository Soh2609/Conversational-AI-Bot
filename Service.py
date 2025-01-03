from flask import Flask,request, jsonify
from Dao import getCustomerID,getAccountBalance
import json

app = Flask(__name__)

@app.route("/getSampleData",methods=['POST'])
def hello():
    print(11)
    response = {
        "fulfillment_response": {
            "messages": [
                {
                    "text": {
                        "text": ["Welcome to B2B python"]
                    }
                }
            ]
        }
    }
    return response#jsonify(response)
    #resp.json={"fulfillment_response":{"messages":[{"text":["Hello from backend"]}]}}
    #return resp 

@app.route("/CBSAPI/getCustomerID",methods=['POST'])
def getCUSTOMERID():
    try:
        #print(request.get_data())
        jsonRequest={}
        jsonrequest=json.loads(request.get_data())
        #print(jsonrequest['queryResult']['name'])
        #return getCustomerID(jsonrequest['queryResult'])
        return getCustomerID(request.get_data())
    except Exception as e:
        return "Error___"+str(e)

@app.route("/CBSAPI/getAccountBalance",methods=['POST'])
def getACCOUNTBalance():
    jsonRequest={}
    jsonrequest=json.loads(request.get_data())
    return getAccountBalance(jsonrequest['queryResult']['parameters'])

@app.route('/webhook',methods=['POST'])
def webhook():
    print('OMKAR')
    #req= request.get_json(silent=True, force=True)
    #print('Request:',req)
    #res= getSampleString(req)
    return {"fulfillmentText":"ABCDEFG"}
def getSampleString(req):
    intent = req.get('queryResult').get('intent').get('displayName')
    if intent == 'Welcome':
       return {"fulfillmentText":"ABCDEFG"}
    #except Exception as e:
    #   return "Error___"+str(e)
#To run the app on WSGI server START
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8084)
    print('Sertver Started')
#To run the app on WSGI server START
