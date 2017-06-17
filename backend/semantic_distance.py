import simplejson as json
import requests

temp = []
with open('data/image_text.json') as infile:
    temp = json.load(infile)['data']

def calculate_semantic_distance(phrase, number):
    global temp
    benchmark_phrases = temp[number]
    sem_score_total = 0
    base_url = "http://swoogle.umbc.edu/StsService/GetStsSim?operation=api&"
    for bp in benchmark_phrases:
        phrase1 = "phrase1="+bp+"&"
        phrase2 = "phrase2="+phrase
        url = base_url + phrase1 + phrase2
        r = requests.get(url)
        res = float(r.text)
        sem_score_total += res
    return sem_score_total/5
