import time, httpx

def solve(site_key = None, proxy=None):
    start_time = time.time()
    k = httpx.post("http://127.0.0.1:5050/solve", timeout=120, json={"proxy": proxy, "site_key": "4c672d35-0701-42b2-88c3-78380b0db560"}).text
    t = round(time.time() - start_time, 2)
    return k, t