import requests
import binascii
import hashlib
import uuid
import datetime
import random

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

class NtLauncher:
    BROWSER_USERAGENT = "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
    DEFAULT_CHROME_VERSION = "C2.1.22.784"
    DEFAULT_GF_VERSION = "2.1.22"
    
    def __init__(self, locale, gfLang, installation_id=None, chromeVersion=None, gfVersion=None, cert=None):
        self.locale = locale
        self.gfLang = gfLang
        self.installation_id = installation_id
        self.chromeVersion = chromeVersion
        self.gfVersion = gfVersion
        self.cert = cert
        self.token = None
        
        if self.chromeVersion == None:
            self.chromeVersion = NtLauncher.DEFAULT_CHROME_VERSION
            
        if self.gfVersion == None:
            self.gfVersion = NtLauncher.DEFAULT_GF_VERSION
            
        if self.cert == None:
            data = pkg_resources.read_binary(__package__, "all_certs.pem")
            start = data.find(b"-----BEGIN CERTIFICATE-----")
            end = data.find(b"-----END CERTIFICATE-----", start)

            self.cert = data[start:end+1+len(b"-----END CERTIFICATE-----")]

    def auth(self, username, password):
        self.username = username
        self.password = password
        
        if not self.installation_id:
            m = hashlib.md5((username + password).encode()).digest()
            self.installation_id = str(uuid.UUID(bytes_le=m)) #it generates just unique uuid for username+password, so others who use this library won't have the same installation_id
            
        if not self.send_start_time():
            return False

        URL = "https://spark.gameforge.com/api/v1/auth/sessions"
        HEADERS = {
            "User-Agent" : NtLauncher.BROWSER_USERAGENT,
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
        
    def send_start_time(self):
        HEADERS = {
            "Host" : "events.gameforge.com",
            "User-Agent" : "GameforgeClient/" + self.gfVersion,
            "Content-Type" : "application/json",
            "Connection" : "Keep-Alive"
        }

        PAYLOAD = """{
    "client_installation_id": "%INSTALLATION_ID%",
    "client_locale": "pol_pol",
    "client_session_id": "%SESSION_ID%",
    "client_version_info": {
        "branch": "master",
        "commit_id": "27942713",
        "version": "%CHROME_VERSION%"
    },
    "id": 0,
    "localtime": "%LOCAL_TIME%",
    "start_count": 1,
    "start_time": %START_TIME%,
    "type": "start_time"
}
        """
        
        payload = PAYLOAD.replace("%INSTALLATION_ID%", self.installation_id)
        payload = payload.replace("%SESSION_ID%", str(uuid.uuid4()))
        payload = payload.replace("%CHROME_VERSION%", self.chromeVersion[1:])
        
        def rreplace(s, old, new, occurrence):
            li = s.rsplit(old, occurrence)
            return new.join(li)

        eu = datetime.timezone(datetime.timedelta(hours=1)) #Eu timezone
        date = datetime.datetime.now(eu)
        date = date.replace(microsecond=0)
        
        payload = payload.replace("%LOCAL_TIME%", rreplace(date.isoformat(), ":", "", 1))
        payload = payload.replace("%START_TIME%", str(random.randint(1500, 10000)))
        
        with pkg_resources.path(__package__, "all_certs.pem") as path:
            certPath = str(path)
        
        r = requests.post("https://events.gameforge.com", headers=HEADERS, data=payload, cert=certPath, verify=certPath)
        
        if r.status_code != 200:
            return False
            
        return True
        
        
    def getAccounts(self):
        if not self.token:
            return False
        
        URL = "https://spark.gameforge.com/api/v1/user/accounts"

        HEADERS = {
            "User-Agent" : NtLauncher.BROWSER_USERAGENT,
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
        
    def getFirstNumber(self, uuid):
        for char in uuid:
            if char.isdigit():
                return char
        
        return None
        
    def generateSecondTypeUserAgentMagic(self):
        firstLetter = self.getFirstNumber(self.installation_id)
        
        if firstLetter == None or int(firstLetter) % 2 == 0:
            hashOfCert = hashlib.sha256(self.cert).hexdigest()
            hashOfVersion = hashlib.sha1(self.chromeVersion.encode("ascii")).hexdigest()
            hashOfInstallationId = hashlib.sha256(self.installation_id.encode("ascii")).hexdigest()
            hashOfSum = hashlib.sha256((hashOfCert + hashOfVersion + hashOfInstallationId).encode("ascii")).hexdigest()
            return hashOfSum[:8]
            
        else:
            hashOfCert = hashlib.sha1(self.cert).hexdigest()
            hashOfVersion = hashlib.sha256(self.chromeVersion.encode("ascii")).hexdigest()
            hashOfInstallationId = hashlib.sha1(self.installation_id.encode("ascii")).hexdigest()
            hashOfSum = hashlib.sha256((hashOfCert + hashOfVersion + hashOfInstallationId).encode("ascii")).hexdigest()
            return hashOfSum[-8:]
        
    def generateThirdTypeUserAgentMagic(self, account_id):
        firstLetter = self.getFirstNumber(self.installation_id)
        firstTwoLettersOfAccountId = account_id[:2]
        
        if firstLetter == None or int(firstLetter) % 2 == 0:
            hashOfCert = hashlib.sha256(self.cert).hexdigest()
            hashOfVersion = hashlib.sha1(self.chromeVersion.encode("ascii")).hexdigest()
            hashOfInstallationId = hashlib.sha256(self.installation_id.encode("ascii")).hexdigest()
            hashOfAccountId = hashlib.sha1(account_id.encode("ascii")).hexdigest()
            hashOfSum = hashlib.sha256((hashOfCert + hashOfVersion + hashOfInstallationId + hashOfAccountId).encode("ascii")).hexdigest()
            return firstTwoLettersOfAccountId + hashOfSum[:8]
            
        else:
            hashOfCert = hashlib.sha1(self.cert).hexdigest()
            hashOfVersion = hashlib.sha256(self.chromeVersion.encode("ascii")).hexdigest()
            hashOfInstallationId = hashlib.sha1(self.installation_id.encode("ascii")).hexdigest()
            hashOfAccountId = hashlib.sha256(account_id.encode("ascii")).hexdigest()
            hashOfSum = hashlib.sha256((hashOfCert + hashOfVersion + hashOfInstallationId + hashOfAccountId).encode("ascii")).hexdigest()
            return firstTwoLettersOfAccountId + hashOfSum[-8:]

    def getToken(self, account, raw=False):
        if not self.token:
            return False
        
        URL = "https://spark.gameforge.com/api/v1/auth/thin/codes"

        HEADERS = {
            "User-Agent" : "Chrome/{} ({}) GameforgeClient/{}".format(self.chromeVersion, self.generateThirdTypeUserAgentMagic(account), self.gfVersion),
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
