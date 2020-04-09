import requests
import binascii
import hashlib
import uuid

class NtLauncher:
    def __init__(self, locale, gfLang, installation_id=None):
        self.locale = locale
        self.gfLang = gfLang
        self.installation_id = installation_id
        self.token = None

    def auth(self, username, password):
        self.username = username
        self.password = password
        
        if not self.installation_id:
            m = hashlib.md5((username + password).encode()).digest()
            self.installation_id = str(uuid.UUID(bytes_le=m)) #it generates just unique uuid for username+password, so others who use this library won't have the same installation_id

        URL = "https://spark.gameforge.com/api/v1/auth/sessions"
        HEADERS = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "TNT-Installation-Id" : self.installation_id,
            "Origin" : "spark://www.gameforge.com",
        }

        CONTENT = {
            "email" : self.username,
            "locale" : self.locale,
            "password" : self.password,
        }

        r = requests.post(URL, headers=HEADERS, json=CONTENT)
        if r.status_code != 201:
            return False
        
        response = r.json()
        self.token = response["token"]

        return True
        
    def getAccounts(self):
        if not self.token:
            return False
        
        URL = "https://spark.gameforge.com/api/v1/user/accounts"

        HEADERS = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "TNT-Installation-Id" : self.installation_id,
            "Origin" : "spark://www.gameforge.com",
            "Authorization" : "Bearer {}".format(self.token),
            "Connection" : "Keep-Alive"
        }

        r = requests.get(URL, headers=HEADERS)

        if r.status_code != 200:
            return False
            
        accounts = []
        response = r.json()
        
        for key in response.keys():
            accounts.append((key, response[key]["displayName"]))

        return accounts

    def _convertToken(self, guid):
        return binascii.hexlify(guid.encode()).decode()

    def getToken(self, account, raw=False):
        if not self.token:
            return False
        
        URL = "https://spark.gameforge.com/api/v1/auth/thin/codes"

        HEADERS = {
            "User-Agent" : "GameforgeClient/2.0.48",
            "TNT-Installation-Id" : self.installation_id,
            "Origin" : "spark://www.gameforge.com",
            "Authorization" : "Bearer {}".format(self.token),
            "Connection" : "Keep-Alive"
        }

        CONTENT = {
            "platformGameAccountId" : account
        }

        r = requests.post(URL, headers=HEADERS, json=CONTENT)

        if r.status_code != 201:
            return False

        if raw:
            return r.json()["code"]
        
        return self._convertToken(r.json()["code"])
