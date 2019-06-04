# NosTale-Auth
Simple library that lets you generate "magic" value for the NoS0577 login packet

# The packet
New login packet `NoS0577` is used when you login with GameForge launcher

That's how it looks like:
`"NoS0577 " + SESSION_GUID + " " + username + " " + INSTALLATION_GUID + " 003662BF" + char(0x0B) + "0.9.3.3103" + " 0 " + MD5_STR(MD5_FILE("NostaleClientX.exe") + MD5_FILE("NostaleClient.exe")`
