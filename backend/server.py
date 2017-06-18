from flask import Flask, request, jsonify
import sys
from utilities import *
from speech_to_text import *
from pprint import pprint
from jsonParser import *
from process_text import *
from classifier import predict_score
import pandas as pd
from tinydb import TinyDB, Query

import random #TODO remove only for testing 

temp = 0
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
    global temp
    session_id = int(body['session_id']) 
    temp = session_id
    image_number = int(body['image_number']) - 1
    res = call_speech_to_text_on_wav(f) 
    res = json.loads(res)
    duration = get_last_timestamp(res)
    whole_transcript = find_transcript(res)
    res = get_feature_vec_default_times(whole_transcript)
    number_of_pauses = res['fillers']
    clean_string = remove_hesitation(whole_transcript) # this string is the transcript of what was said without %HESITATION
    number_of_grammar_errors = grammar_suggestions(clean_string)['number_of_grammar_errors']
    row = dictionary2row(res)
    row[-1] = number_of_grammar_errors
    score = predict_score(row)[0]
    score = list(score) #from the model 
    semantic_score = calculate_semantic_distance(clean_string,image_number) 
    
    specific_sess = sess.search(Sess.session_id == session_id)
    if len(specific_sess)>0:
        lst1 = specific_sess[0]['model_scores']
        lst1.append(score)
        lst2 = specific_sess[0]['semantic_scores']
        lst2.append(semantic_score)
        lst3 = specific_sess[0]['durations']
        lst3.append(duration)
        lst4 = specific_sess[0]['nop']
        lst4.append(number_of_pauses)
        lst5 = specific_sess[0]['noge']
        lst5.append(number_of_grammar_errors)
        sess.update({'model_scores' : lst1, 'semantic_scores' : lst2, 'durations' : lst3, 'nop' : lst4,'noge' : lst5}, Sess.session_id == session_id)
    else:
        sess.insert({'session_id' : session_id,  'model_scores' : [score] , 'semantic_scores' : [semantic_score] , 'durations' : [duration], 'nop' : [number_of_pauses], 'noge' : [number_of_grammar_errors]  })
    
    return jsonify({"result"  : "success"})

@app.route('/get_results')
def get_results():
    body = request.form
    # session_id = int(body['session_id'])
    global temp
    session_id = temp
    specific_sess = sess.search(Sess.session_id == session_id)[0]
    semantic_scores = specific_sess['semantic_scores'][:4]
    noge = specific_sess['noge'][:4]
    model_scores = specific_sess['model_scores'][:4]
    final_list = []
    for m in model_scores:
        final_list.append(m[0])
    final_sem_score = sum(semantic_scores)/len(semantic_scores)
    final_noge_score = sum(noge)/len(noge)
    final_model_score = sum(final_list)/len(final_list)    

    final_score = 0.5*final_model_score + 0.2*final_noge_score + 0.3*final_sem_score

    total_duration = sum(specific_sess['durations'][:4])
    number_of_pauses = sum(specific_sess['nop'][:4])

    res = {"score" : final_score, "duration" : total_duration, "number_of_pauses" : number_of_pauses}

    return jsonify(res)

if __name__ == "__main__":
    app.run(debug=True, host=HOST, port=17001, threaded=True)
