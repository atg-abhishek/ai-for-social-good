import json
import sys
from pprint import pprint

def parse():
    with open('data/speech_to_text.json') as data_file:
        data = json.load(data_file)
        result = findKey(data, 'transcript')
        print "Final: ", result
        # pprint(data.items())

def findKey(dictionary, key):
    # print "dragon"
    # print dictionary.keys()
    result = ""
    if key in dictionary.keys():
        # result += dictionary[key]
        # return
        return dictionary[key]

    for k in dictionary.keys():
        v = dictionary[k]
        if isinstance(v, list):
            for listItem in v:
                if isinstance(listItem, dict):
                    requiredVal = findKey(listItem, key)
                    if requiredVal is not None:
                        result += requiredVal
                        # print "1. ", result
                        # print "Val: ", requiredVal
                    # if requiredVal is not None:
                    #     result += requiredVal
                    # if requiredVal is not None:
                    #     return requiredVal
    # print "2. ", result
    return result


def main():
    parse()

main()