import os, json

for name in os.listdir('riddles'):
    with open("riddles/" + name) as f:
        data = json.load(f)
