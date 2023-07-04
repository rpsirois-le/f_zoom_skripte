from pysqlcipher3 import dbapi2 as sqlcipher from Crypto.Cipher import AES
from Crypto.Hash import SHA256
import binascii
from base64 import b64decode
from base64 import b64encode
import win32crypt
import os

debug=0
accountDBPath="clxzqi4tthacxaxx2_aola@xmpp.zoom.us"

#read the key from file
zoomIni = "Zoom.us.ini"
zoomKey = "zoomKey.txt"

with open(zoomIni,'r+b') as fent:
    raw_key = fent.read()

if debug : print("raw_key:")
if debug : print(raw_key)

length = len(raw_key)
if debug : print("raw len: ",length)

#remove the trailing characters "[ZoomChat] win_osencrypt_key=ZWOSKEY"
b64 = raw_key[37:length]
if debug : print("b64:")
if debug : print(b64)

#base64 decode
enc_key = b64decode(b64)
if debug : print("enc_key:")
if debug : print(binascii.hexlify(enc_key))

#decrypt the key which is dpapi encrypted
entropy = None
ps = None
flags = 0

key = win32crypt.CryptUnprotectData(enc_key, entropy, None, ps, flags)

Masterkey=key[1][0:42]
print("Masterkey[42]:<"+Masterkey+">")

# read Accountkey (KWK) from file ... needs to be provided
accountKeyFile = accountDBPath+"/key.txt"
with open(accountKeyFile,'r+b') as fent:
    accountKey = fent.read()

print("accountKey[44]:<"+accountKey+">")
print("accountKey decoded[32]:<"+binascii.hexlify(b64decode(accountKey))+">")

#build key for the encryted fields
h1 = SHA256.new()
h1.update(Masterkey)
masterSHA = binascii.unhexlify(h1.hexdigest())
if debug : print("masterSHA 0x[32]:<"+binascii.hexlify(masterSHA)+">")

h2 = SHA256.new()
h2.update(accountKey)
accountSHA = binascii.unhexlify(h2.hexdigest())
if debug : print("accountSHA 0x[32]:<"+binascii.hexlify(accountSHA)+">")

h3 = SHA256.new()
h3.update(masterSHA+accountSHA)
finalSHA = binascii.unhexlify(h3.hexdigest())
if debug : print("finalSHA 0x[32]:<"+binascii.hexlify(finalSHA)+">")

accountDBKey = b64encode(finalSHA) print("accountDBKey [44]:<"+accountDBKey+">")
keystr='pragma key="'+accountDBKey+'"' if debug : print(keystr)

# create folder for the decrypted databases and decrypt and clone the DBs
if not os.path.exists(accountDBPath+'/dec'):
    os.makedirs(accountDBPath+'/dec')
    print("creating dec folder")
