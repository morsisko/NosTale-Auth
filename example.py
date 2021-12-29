from nosauth import api

api = api.NtLauncher(locale='pl_PL', gfLang='pl')

if not api.auth(username='admin', password='admin'):
    print('Couldn\'t auth!')
    exit()
    
accounts = api.getAccounts()
if not len(accounts):
    print('You don\'t have any any account')
    
for uid, displayName in accounts:
    print(f'Account key: {uid} Account name: {displayName}')

uid, displayName = accounts[0]
token = api.getToken(uid)

if token:
    print(token)

else:
    print('Couldn\'t obtain token!')

