import json

with open('usnews_data.json') as f:
    d = json.load(f)


print(d)