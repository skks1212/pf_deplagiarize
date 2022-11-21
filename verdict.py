import requests
import os
import json
from lavenshtein import percent_diff
from os.path import exists

def get_verdict(github_link : str, level = 4, cutoff : int = 20):
    strip_github_link = github_link.split("github.com/")[1]
    test_link = "https://raw.githubusercontent.com/" + strip_github_link + "/main/"

    if requests.get(test_link).status_code == 200:
        raw_link = test_link
    else :
        raw_link = "https://raw.githubusercontent.com/" + strip_github_link + "/master/"
    
    path_to_json = 'patterns/' + str(level) + '/'
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')] 

    for pattern in json_files:
        with open(os.path.join(path_to_json, pattern)) as f:
            data = json.load(f)
            
            print("Checking similarities with " + data["name"])

            files = data["files"]

            for file in files.keys():
                submitted = requests.get(raw_link + file).text
                pattern_dir = os.path.dirname(__file__) + "/source/" + data["name"] + "/"

                if not exists(pattern_dir):
                    os.makedirs(pattern_dir)

                source = pattern_dir + file.replace("/", "_")

                if not exists(source):
                    with open(source, "w") as f:
                        f.write(requests.get(files[file]).text)

                with open(source) as f:
                    control = f.read()

                diff = percent_diff(submitted, control)

                if diff < cutoff:
                    print("SIMILARITY FOUND -- " + data["name"] + " = " + str(100 - diff) + "%")
                    return {
                        "name": data["name"],
                        "percent": round(100 - diff, 2),
                        "verdict" : True,
                        "message" : data["description"]
                    }
    
    return {
        "name": "Original",
        "percent": 0,
        "verdict" : False,
        "message" : "No plagiarism found"
    }