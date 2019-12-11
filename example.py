from ntauth import loginapi

api = loginapi.NtLauncher(locale="pl_PL", gfLang="pl", installation_id="5ea61643-b22a-4ad6-89dd-175b0be2c9d9")

if not api.auth(username="admin", password="admin"):
    print("Couldn't auth!")
    exit()
    
accounts = api.getAccounts()
token = api.getToken(accounts[0])

if token:
    print(token)

else:
    print("Couldn't obtain token!")

