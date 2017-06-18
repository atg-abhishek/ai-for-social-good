import json
import sys
from pprint import pprint

def parse():
    with open('data/speech_to_text.json') as data_file:
        data = json.load(data_file)
        result = findKey(data, 'transcript')
        for x in range(len(result)):
            for y in range(len(result[x])):
                result[x][y] = str(result[x][y])

        pprint(result)

def findKey(dictionary, key):
    result = ""
    if key == "timestamps":
        result = []
    if key in dictionary.keys():
        return dictionary[key]

    for k in dictionary.keys():
        v = dictionary[k]
        if isinstance(v, list):
            for listItem in v:
                if isinstance(listItem, dict):
                    requiredVal = findKey(listItem, key)
                    if requiredVal is not None:
                        result += requiredVal

    return result

def find_transcript(dictionary):
    temp = ""
    res = dictionary['results']
    for row in res:
        temp += row['alternatives'][0]['transcript']

    return temp

def get_last_timestamp(dictionary):
    res = dictionary['results']
    if len(res) == 0:
        return 0.0
    last = res[len(res) - 1]['alternatives']
    pprint(last)
    last = last[0]['timestamps']
    if len(last) == 0:
        return 0.0
    last_word = last[len(last) - 1]
    return float(last_word[2])
