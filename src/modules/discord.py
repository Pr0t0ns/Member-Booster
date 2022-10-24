import json, ssl
from .client import getClient

class Discord:
    def __init__(self, ja3, user_agen, sup_prop):
        self.ja3 = ja3
        self.user_agent = user_agen
        self.sup_prop = sup_prop
    
    
    def getLocaleAndConsent(self, proxy):
        prox = {
        "http://": "http://" + str(proxy),
        "https://": "http://" + str(proxy),
        }
        s = getClient(proxies=prox)

        r = json.loads(s.get("https://discord.com/api/v9/auth/location-metadata", proxies=prox).text)
        consent = r["consent_required"]
        country_code = r["country_code"]
        return consent, country_code

    def generateToken(self, cap, proxy, username, invite):
        prox = {
        "http://": "http://" + str(proxy),
        "https://": "http://" + str(proxy),
        }
        #consent, country_code = self.getLocaleAndConsent(proxy)

        s = getClient(proxies=prox)

        d = {
            "fingerprint": s.headers["x-fingerprint"],
            "username": username,
            "consent": True,
            "captcha_key": cap,
            "invite": invite
        }
        s.headers["content-length"] = str(len(json.dumps(d)))

        r = s.post("https://discord.com/api/v10/auth/register", json=d)
        res = json.loads(r.text)
        token = res['token']
        return token

    def checkIfLocked(self, proxy, token):
        prox = {
        "http://": "http://" + str(proxy),
        "https://": "http://" + str(proxy)
        }
        #consent, country_code = self.getLocaleAndConsent(proxy)
        s = getClient(proxies=prox)
        s.headers["authorization"] = token

        r = s.get('https://discord.com/api/v9/users/@me/library')
        if r.status_code == 401 or r.status_code == 403:
            return True, r.status_code
        else:
            return False, r.status_code

    def checkFlags(self, proxy, token):
        prox = {
        "http://": "http://" + str(proxy),
        "https://": "http://" + str(proxy)
        }
        s = getClient(proxies=prox)
        s.headers["authorization"] = token

        r = json.loads(s.get('https://discord.com/api/v9/users/@me').text)
        flag = r['public_flags']
        return flag
