# _*_ coding utf-8 _*_
__author__ = 'Xu Kartmann'
__date__ = '20/08/2019'

from flask import Flask, request, make_response, jsonify
from intent_solver import QueryFactory
from nlpmodel import NlpModel
from utils import isScreen_output_capable

app = Flask(__name__)


@app.route('/', methods=['POST'])
def web_hook():
    req = request.get_json(force=True)
    query_parser.frontend = "action" if isScreen_output_capable(req) else "default"

    response = {"fulfillmentText": "Sorry, I don't understand that."}
    if req["queryResult"]["queryText"] == "GOOGLE_ASSISTANT_WELCOME":
        return make_response(jsonify({"fulfillmentText":
                                          "Good day! Welcome to Night Safari. What can I do for you today?"}))
    if req["queryResult"]["intent"]["displayName"] != "Default Fallback Intent":
        query_parser.order(req["queryResult"]["parameters"], req["queryResult"]["intent"]["displayName"])
        response = query_parser.parse()

    # FAQ intents
    if req["queryResult"]["intent"]["displayName"] == "Default Fallback Intent" or (isinstance(response, str) and response == ""):
        print("fallback")
        t = nlp.response(req['queryResult']['queryText']).split('\n')
        print('mwzoutput:', t)
        if len(t) > 1:
            t = t[1]
        print('mwzoutputfinal:', t)
        response = {"fulfillmentText": t}

    return make_response(jsonify(response))


if __name__ == '__main__':
    nlp = NlpModel()
    query_parser = QueryFactory(datafile="..\\data\\night_safari.json")
    app.run(debug=True, host='0.0.0.0', port=4300)
