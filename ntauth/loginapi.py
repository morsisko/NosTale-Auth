import requests
import binascii

class NtLauncher:
    def __init__(self, locale, gfLang, installation_id):
        self.locale = locale
        self.gfLang = gfLang
        self.installation_id = installation_id
        self.token = None
        self.platformGameAccountId = None

    def auth(self, username, password):
        self.username = username
        self.password = password

        URL = "https://spark.gameforge.com/api/v1/auth/thin/sessions"
        HEADERS = {
            "User-Agent" : "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
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
        self.platformGameAccountId = response["platformGameAccountId"]

        return True

    def _convertToken(self, guid):
        return binascii.hexlify(guid.encode()).decode()

    def getToken(self):
        if not self.token or not self.platformGameAccountId:
            return False
        
        URL = "https://spark.gameforge.com/api/v1/auth/thin/codes"

        HEADERS = {
            "User-Agent" : "TNTClientMS2/1.3.39",
            "TNT-Installation-Id" : self.installation_id,
            "Origin" : "spark://www.gameforge.com",
            "Authorization" : "Bearer {}".format(self.token),
            "Connection" : "Keep-Alive"
        }

        CONTENT = {
            "platformGameAccountId" : self.platformGameAccountId
        }

        r = requests.post(URL, headers=HEADERS, json=CONTENT)

        if r.status_code != 201:
            return False

        return self._convertToken(r.json()["code"])
