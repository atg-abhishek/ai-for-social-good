from flask import Flask, request, jsonify
import sys
from utilities import *
from speech_to_text import *
from pprint import pprint
from jsonParser import find_transcript
from process_text import get_feature_vec_default_times, dictionary2row
from classifier import predict_score
import pandas as pd
from tinydb import TinyDB, Query

import random #TODO remove only for testing 

DB_ADDRESS = "db.json"
HOST = None
app = Flask(__name__)
db = TinyDB(DB_ADDRESS)
Sess = Query()
sess = db.table('sess')

if len(sys.argv)>1 and sys.argv[1] == "prod":
    HOST = '0.0.0.0'

@app.route('/')
def hello():
    return "SERVER CRASHEDDDD OHNOOOOO!!!!"

@app.route('/raw_audio', methods=['POST'])
def raw_audio():
    if 'file' not in request.files:
        return "There was no file attached"
    f = request.files['file']
    body = request.form
    session_id = body['session_id'] #TODO  tell Arun
    image_number = body['image_number'] #TODO: Arun
    res = call_speech_to_text_on_wav(f) 
    res = json.loads(res)
    whole_transcript = find_transcript(res)
    res = get_feature_vec_default_times(whole_transcript)
    row = dictionary2row(res)
    score = predict_score(row)[0]
    specific_sess = sess.search(Sess.session_id == session_id)
    if len(specific_sess)>0:
        lst = specific_sess['scores']
        lst.append(score)
        sess.update({'scores' : lst}, Sess.session_id == session_id)
    else:
        sess.insert({'session_id' : session_id, 'scores' : [score]})
    
    # TODO : calculate final score 

    return jsonify({"result"  : res})

@app.route('/get_results')
def get_results():
    score = random.uniform(0,1)
    duration = random.uniform(30, 120)
    number_of_pauses = random.randint(0,25)

    res = {"score" : score, "duration" : duration, "number_of_pauses" : number_of_pauses}

    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=17001, threaded=True)
