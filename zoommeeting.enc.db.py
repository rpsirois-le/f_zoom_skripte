from pysqlcipher3 import dbapi2 as sqlcipher
import binascii
from base64 import b64decode
import win32crypt
import os

debug=1
encDB="zoommeeting.enc.db"
decDB="dec/zoommeeting.db"

#remove old decrypted DB
if os.path.exists(decDB):
  os.remove(decDB)
    print("old db "+decDB+" removed")
else:
    print("The file "+decDB+" does not exist")

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

print("Masterkey:<"+key[1]+">")
#prepare SQL Statement
Masterkey=key[1]
keystr='pragma key="'+Masterkey+'"'
print(keystr)
#connect to the database an decrypt with Mastekey
db = sqlcipher.connect(encDB)
db.execute(keystr)
db.execute('PRAGMA kdf_iter = "4000"')
db.execute('PRAGMA cipher_page_size = 1024') print(db.execute('SELECT count(*) FROM sqlite_master').fetchall())

#copy DB
db.execute('ATTACH DATABASE "dec/zoommeeting.db" AS zoom KEY ""') db.execute('SELECT sqlcipher_export("zoom")')
db.execute('DETACH DATABASE zoom')
db.close()
