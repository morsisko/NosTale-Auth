import requests
import binascii

class NtLauncher:
    def __init__(self, locale, gfLang, installation_id):
        self.locale = locale
        self.gfLang = gfLang
        self.installation_id = installation_id
        self.token = None
        self.platformUserId = None

    def auth(self, username, password):
        self.username = username
        self.password = password

        URL = "https://spark.gameforge.com/api/v1/auth/thin/sessions"
        HEADERS = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36",
            "TNT-Installation-Id" : self.installation_id,
            "Origin" : "spark://www.gameforge.com"
        }

        CONTENT = {
            "gfLang" : self.gfLang,
            "identity" : self.username,
            "locale" : self.locale,
            "password" : self.password,
            "platformGameId" : "dd4e22d6-00d1-44b9-8126-d8b40e0cd7c9"
        }

        r = requests.post(URL, headers=HEADERS, json=CONTENT)
        if r.status_code != 201:
            return False
        
        response = r.json()
        self.token = response["token"]
        self.platformUserId = response["platformUserId"]

        return True
        
    def getAccounts(self):
        if not self.token or not self.platformUserId:
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
        if not self.token or not self.platformUserId:
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
