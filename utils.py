
import json

def save_j(obj, file):
    try:
        j = json.dumps(obj)
        f = open(file, "w")
        f.write(j)
        f.close()
    except IOError:
        print("Could not save files")

def load_j(file):
    try:
        with open(file) as f:
            data = json.load(f)
        return data
    except:
        return {}



