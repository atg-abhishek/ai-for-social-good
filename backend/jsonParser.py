import json
import sys
from pprint import pprint

def parse():
    with open('jsonData.json') as data_file:
        data = json.load(data_file)
        result = findKey(data, 'transcript')
        print result
        # pprint(data.items())

def findKey(dictionary, key):
    # transcriptDictionary = {}
    if key in dictionary:
        return dictionary[key]
    for k, v in dictionary.items():
        if isinstance(v,dict):
            item = findKey(v, key)
            if item is not None:
                return item


parse()