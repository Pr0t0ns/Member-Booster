from flask import Flask, request
import json, httpx
from undetected_chromedriver import Chrome, ChromeOptions

app = Flask(__name__)

@app.route("/", methods=['POST'])
def hsw():
    data = json.loads(request.data)
    c = data['c']
    m = data["m"]
    hsw_code = m
    hsw = driver.execute_script(f"{hsw_code}; return hsw('{c}')")
    return hsw

if __name__ == "__main__":
    print("Starting")
    chrome_opts = ChromeOptions()
    chrome_opts.arguments.extend(["--no-sandbox", "--disable-setuid-sandbox", "--headless", "--disable-dev-shm-usage", "--disable-accelerated-2d-canvas", "--no-zygote", "--disable-gpu", "--load-extension=C:\\Users\\macie\\Documents\\Discord Projects\\Member Booster\\src\\hsw_server\\extensions\\fingerprint_extention"]) 
    driver = Chrome(options=chrome_opts)
    app.run("127.0.0.1", port=8080)