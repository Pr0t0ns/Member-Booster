import datetime
import httpx
import urllib.request
from python_ghost_cursor import path
import json
import base64
import random
import time
import string
from .hcaptcha import core



class Solver:
  def __init__(self, proxy, url="discord.com", site_key="4c672d35-0701-42b2-88c3-78380b0db560", headless=True):
    self.sitekey = site_key
    self.href = url
    self.host = url.replace("https://", "").replace("http://", "")
    if "/" in self.host and not self.host.startswith("/"):
      self.host = self.host.split("/")[0]
    if proxy != None:
        self.client = httpx.Client(proxies={'http://': f'http://{proxy}', 'https://': f'http://{proxy}'}, timeout=120)
    else:
        self.client = httpx.Client(timeout=120)

    self.userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.141 Whale/3.15.136.29 Safari/537.36"
    self.version = self.client.get("https://hcaptcha.com/1/api.js?render=explicit&onload=hcaptchaOnLoad", headers={
        "user-agent": self.userAgent,
        "referer": self.host,
        "accept-language": "en-US,en;q=0.9",
        "accept": "*/*",
        "sec-fetch-dest": "script",
        "sec-ch-ua-platform": "\"Windows\""
    }).text.split("assetUrl")[1].split("https://newassets.hcaptcha.com/captcha/v1/")[1].split("/static")[0]
    self.headless = headless

  def _getHsw(self, m, c):
    hsw = httpx.post("http://127.0.0.1:8080/", json={"c":c, "m": m}, timeout=15)
    return hsw.text

  def _getCaptcha(self):
    start = {'x': 100, 'y': 100}
    end = {'x': 600, 'y': 700}
    timestamp = int((time.time() * 1000) + round(random.random() * (120 - 30) + 30))
    mm = [[int(p['x']), int(p['y']), int(time.time() * 1000) + round(random.random() * (5000 - 2000) + 2000)] for p in path(start, end)]

    o = json.loads(self.client.post(f"https://hcaptcha.com/checksiteconfig?v={self.version}&host={self.host}&sitekey={self.sitekey}&sc=1&swa=1", headers={
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        "content-type": "text/plain",
        "origin": "https://newassets.hcaptcha.com",
        "referer": "https://newassets.hcaptcha.com/",
        "user-agent": self.userAgent,
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }).text)
    l = json.loads(base64.b64decode(
        str((o["c"]["req"].split(".")[1]) + ("=" * 8)).encode()).decode())["l"]
    self.s = self.client.get(f"{l}/hsw.js", headers={
        "user-agent": self.userAgent,
        "referer": f"https://newassets.hcaptcha.com/captcha/v1/{self.version}/static/hcaptcha.html",
        "accept-language": "en-US,en;q=0.9",
        "accept": "*/*"
    }).text
    h = self._getHsw(self.s, o["c"]["req"])
    w = "".join(random.choice(string.ascii_lowercase) for i in range(12))
    p = {
        "v": self.version,
        "sitekey": self.sitekey,
        "host": self.host,
        "hl": "en",
        "motionData": json.dumps({"st": timestamp, "dct": timestamp, "mm": mm}),
        "n": h,
        "c": "{\"type\":\"" + o["c"]["type"] + "\",\"req\":\"" + o["c"]["req"] + "\"}"
    }
    c = self.client.post(f"https://hcaptcha.com/getcaptcha/{self.sitekey}", headers={
        "accept": "application/json",
        "accept-language": "en-US,en;q=0.9",
        #"content-length": str(len(p)),
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://newassets.hcaptcha.com",
        "referer": "https://newassets.hcaptcha.com/",
        "user-agent": self.userAgent,
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }, data=p).json()
    return c


  def get_as_base64_without(img_url):
    headers = {
        "Authority": "hcaptcha.com",
        "Accept": "application/json",
        "Accept-Language": "en-US,en;q=0.9",
        "Content-Type": "application/json",
        "Origin": "https://newassets.hcaptcha.com/",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "User-Agent": headers,
    }
    return base64.b64encode(httpx.get(img_url, headers=headers).content)

  def solveCaptcha(self):
    c = self._getCaptcha()     
    try:
      k, t = c["key"], c["tasklist"]
    except:
      if c.get("generated_pass_UUID"):
        return c["generated_pass_UUID"]
    i, t_, z = {}, {}, 0
    g = c["requester_question"]["en"].replace("Please click each image containing a ", "")
    g = g.replace("Please click each image containing an ", "")
    g = g.strip(".")
    images_task = []

    for u in t:
        url, task_key = str(u["datapoint_uri"]), str(u["task_key"])
        image = urllib.request.urlopen(url).read()
        images_task.append([image, task_key])
    
    hc = core.ArmorCaptcha(label=g)
    a = hc.challenge(images_task)
    h = self._getHsw(self.s, c["c"]["req"])
    start = {'x': 100, 'y': 100}
    end = {'x': 600, 'y': 700}
    timestamp = int((time.time() * 1000) + round(random.random() * (120 - 30) + 30))
    mm = [[int(p['x']), int(p['y']), int(time.time() * 1000) + round(random.random() * (5000 - 2000) + 2000)] for p in path(start, end)]
    s = {
            "v": self.version,
            "job_mode": "image_label_binary",
            "answers": a,
            "serverdomain": self.host,
            "sitekey": self.sitekey,
            "motionData": json.dumps({"st": timestamp, "dct": timestamp, "mm": mm}),
            "n": h,
            "c": "{\"type\":\"" + c["c"]["type"] + "\",\"req\":\"" + c["c"]["req"] + "\"}"
    }; s["motionData"] = s["motionData"].replace("1661664", str(round(datetime.datetime.now().timestamp()))[:7])
   
    sv = self.client.post(f"https://hcaptcha.com/checkcaptcha/{self.sitekey}/{k}",timeout=15, json=s, headers={
            "Authority": "hcaptcha.com",
            "content-type": "application/json",
            "accept-language": "en-US,en;q=0.9",
            #"content-length": str(len(s)),
            "accept": "*/*",
            "origin": "https://newassets.hcaptcha.com",
            "referer": "https://newassets.hcaptcha.com/",
            "user-agent": self.userAgent,
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site"
    }).text
    if "generated_pass_UUID" in sv: return json.loads(sv)["generated_pass_UUID"]
    else: return False

def main(proxy, site_key="4c672d35-0701-42b2-88c3-78380b0db560"):
    solver = Solver(proxy, site_key=site_key)
    result = solver.solveCaptcha()
    return result
    