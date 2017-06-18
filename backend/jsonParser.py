import json
import sys
from pprint import pprint

def parse():
    with open('data/speech_to_text3.json') as data_file:
        data = json.load(data_file)
        result = findKey(data, 'timestamps')
        for x in range(len(result)):
            for y in range(len(result[x])):
                result[x][y] = str(result[x][y])

        pprint(result)

def findKey(dictionary, key):
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

parse()