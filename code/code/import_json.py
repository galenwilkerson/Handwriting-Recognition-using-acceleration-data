import json

filename = "../data/unsegmented/picgold_2014-09-08T16_47_05.674687_pen.json"

with open(filename) as json_file:
    json_data = json.load(json_file)
    print(json_data)
