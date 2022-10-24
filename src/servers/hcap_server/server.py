from flask import Flask, request
import itertools
import json

from src.slvr import main

app = Flask(__name__)

@app.route("/solve", methods=['POST'])
def solve():
    data = json.loads(request.data)
    t = 0
    k = False
    while k == False:
        if t == 3:
            return "False"
        
        try:
            k = main(proxy=data["proxy"], site_key=data["site_key"])
        except:
            return "False"
        
        t += 1
    return k

if __name__ == "__main__":
    app.run("127.0.0.1", port=5050)