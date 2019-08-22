#!/usr/bin/env python

from flask_assistant import request as req
import requests
from nlpmodel import NlpModel
from intent_solver import QueryFactory
import logging
from flask import Flask
from flask_assistant import Assistant, ask, tell, context_manager

import warnings
warnings.filterwarnings("ignore")

project_id='zooq-a-laoaju'
app = Flask(__name__)
assist = Assistant(app, route='/', project_id = project_id)
#logging.getLogger('flask_assistant').setLevel(logging.DEBUG)


@assist.action('Default Fallback Intent')
def safariFallbackQA():
    user_query = req['queryResult']['queryText']
    return tell(nlp.response(user_query))

@assist.action('getUserAddr')
def getUserAddr():
    query.order(req['queryResult']['parameters'])
    return tell(query.parse())

@assist.action('Navigate')
def navigate():
    query.order(req['queryResult']['parameters'])
    return tell(query.parse())

@assist.action('nightsafariIntentSolver')
def nightsafariIntentSolver():
    query.order(req['queryResult']['parameters'])
    t = query.parse()
    if t.strip() == '':
        t = nlp.response(req['queryResult']['queryText']).split('\n')
        print('mwzoutput:',t)
        if len(t) > 1:
            t = t[1]
        print('mwzoutputfinal:',t)
    return tell(t)



import time
def print_timestamp():
    ct = time.time()
    local_time = time.localtime(ct)
    data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    data_msecs = (ct - int(ct)) * 1000
    time_stamp = "%s.%03d" % (data_head, data_msecs)
    print(time_stamp)
    return time_stamp



if __name__ == "__main__":
    nlp = NlpModel()
    nlp.response("") #to speed up sequence call
    query = QueryFactory()
    print('server start')
    app.run(debug=True, host="localhost", port=8080)
