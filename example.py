from ntauth import loginapi

api = loginapi.NtLauncher(locale="pl_PL", gfLang="pl", installation_id="5ea61643-b22a-4ad6-89dd-175b0be2c9d9")

if not api.auth(username="admin", password="admin"):
    print("Couldn't auth!")
    exit()
    
accounts = api.getAccounts()
if len(accounts) == 0:
    print("You don't have any any account")
    
for uid, displayName in accounts:
    print("Account key:", uid, "Account name:", displayName)

uid, displayName = accounts[0]
token = api.getToken(uid)

if token:
    print(token)

else:
    print("Couldn't obtain token!")

