import os
import binascii
import win32crypt

from base64 import b64decode
from pysqlcipher3 import dbapi2 as sqlcipher from Crypto.Cipher import AES
from Crypto.Hash import SHA256

debug=1

if debug : print("debug an")

def decField(content):
    #decode and decrypt UID field
    raw = b64decode(content)
    if debug : print("raw: ",binascii.hexlify(raw))

    length = len(raw)
    if debug : print("raw len: ",length)

    iv = raw[1:13]
    tag = raw[(length-16):(length)]
    data = raw[19:(length-16)]

    if debug : print("iv: ",binascii.hexlify(iv))
    if debug : print("tag: ",binascii.hexlify(tag))
    if debug : print("data: ",binascii.hexlify(data))

    cipher = AES.new(fieldkey,AES.MODE_GCM,iv)

    #decryption with tag verification
    plaintext = cipher.decrypt_and_verify(data,tag)
    #print("text: ",plaintext)
    return plaintext

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
#print(key[1])

Masterkey=key[1]

#save the key to a file
with open(zoomKey,'w+b') as fout:
    fout.write(key[1])

#decypt the database with the key
keystr='pragma key="'+Masterkey+'"'
if debug : print(keystr)

db = sqlcipher.connect('zoomus.enc.db')
db.execute(keystr)
db.execute('PRAGMA kdf_iter = "4000"')
db.execute('PRAGMA cipher_page_size = 1024')
if debug : print(db.execute('SELECT count(*) FROM sqlite_master').fetchall())

#copy content of zoomus.enc.db to an unencrypted DB
if not os.path.exists('dec'):
    os.makedirs('dec')
    print("creating dec folder")

if os.path.exists("dec/zoomus.db"):
    os.remove("dec/zoomus.db")
    print("old dec/zoomus.db removed")
else:
    print("The file dec/zoomus.db does not exist")

db.execute('ATTACH DATABASE "dec/zoomus.db" AS zoom KEY ""')
db.execute('SELECT sqlcipher_export("zoom")')
db.execute('DETACH DATABASE zoom')
db.close()
db = sqlcipher.connect('dec/zoomus.db')

#build key for the encryted fields
h = SHA256.new()
h.update(Masterkey)
fieldkey = binascii.unhexlify(h.hexdigest())

print("fieldkey:<"+binascii.hexlify(fieldkey)+">")

#get decrypted fields

#UID
usr_acc=db.execute('select uid FROM zoom_user_account_enc').fetchall()
if debug : print(usr_acc)
uid = decField(usr_acc[0][0])
if debug : print("UID: "+uid)
keystr='UPDATE zoom_user_account_enc SET uid ="'+uid+'"'
if debug : print(keystr)
db.execute(keystr)

#uname
usr_acc=db.execute('select uname FROM zoom_user_account_enc').fetchall()
if debug : print(usr_acc)
uname = decField(usr_acc[0][0])
if debug : print("uname: "+uname)
keystr='UPDATE zoom_user_account_enc SET uname ="'+uname+'"'
if debug : print(keystr)
db.execute(keystr)

#zoom_uid
usr_acc=db.execute('select zoom_uid FROM zoom_user_account_enc').fetchall()
if debug : print(usr_acc)
zoom_uid = decField(usr_acc[0][0])
if debug : print("zoom_uid: "+zoom_uid)
keystr='UPDATE zoom_user_account_enc SET zoom_uid ="'+zoom_uid+'"'
if debug : print(keystr)
db.execute(keystr)

#account_id
usr_acc=db.execute('select account_id FROM zoom_user_account_enc').fetchall()
if debug : print(usr_acc)
account_id = decField(usr_acc[0][0])
if debug : print("account_id: "+account_id)
keystr='UPDATE zoom_user_account_enc SET account_id ="'+account_id+'"'
if debug : print(keystr)
db.execute(keystr)

#credForNOS
usr_acc=db.execute('select credForNOS FROM zoom_user_account_enc').fetchall()
if debug : print(usr_acc)
credForNOS = decField(usr_acc[0][0])
if debug : print("credForNOS: "+credForNOS)
keystr='UPDATE zoom_user_account_enc SET credForNOS ="'+credForNOS+'"'
if debug : print(keystr)
db.execute(keystr)

#recommendEmailSubject
usr_acc=db.execute('select recommendEmailSubject FROM zoom_user_account_enc').fetchall()
if debug : print(usr_acc)
recommendEmailSubject = decField(usr_acc[0][0])
if debug : print("recommendEmailSubject: "+recommendEmailSubject)
keystr='UPDATE zoom_user_account_enc SET recommendEmailSubject ="'+recommendEmailSubject+'"'
if debug : print(keystr)
db.execute(keystr)

#recommendEmailBody
usr_acc=db.execute('select recommendEmailBody FROM zoom_user_account_enc').fetchall()
if debug : print(usr_acc)
recommendEmailBody = decField(usr_acc[0][0])
if debug : print("recommendEmailBody: "+recommendEmailBody)
keystr='UPDATE zoom_user_account_enc SET recommendEmailBody ="'+recommendEmailBody+'"'
if debug : print(keystr)
db.execute(keystr)

#zoomRefreshToken
usr_acc=db.execute('select zoomRefreshToken FROM zoom_user_account_enc').fetchall()
if debug : print(usr_acc)
zoomRefreshToken = decField(usr_acc[0][0])
if debug : print("zoomRefreshToken: "+zoomRefreshToken)
keystr='UPDATE zoom_user_account_enc SET zoomRefreshToken ="'+zoomRefreshToken+'"'
if debug : print(keystr)
db.execute(keystr)

#zoomEmail
usr_acc=db.execute('select zoomEmail FROM zoom_user_account_enc').fetchall()
if debug : print(usr_acc)
zoomEmail = decField(usr_acc[0][0])
if debug : print("zoomEmail: "+zoomEmail)
keystr='UPDATE zoom_user_account_enc SET zoomEmail ="'+zoomEmail+'"'
if debug : print(keystr)
db.execute(keystr)

#snsID
usr_acc=db.execute('select snsID FROM zoom_user_account_enc').fetchall()
if debug : print(usr_acc)
snsID = decField(usr_acc[0][0])
if debug : print("snsID: "+snsID)
keystr='UPDATE zoom_user_account_enc SET snsID ="'+snsID+'"'
if debug : print(keystr)
db.execute(keystr)

#firstName
usr_acc=db.execute('select firstName FROM zoom_user_account_enc').fetchall()
if debug : print(usr_acc)
firstName = decField(usr_acc[0][0])
if debug : print("firstName: "+firstName)
keystr='UPDATE zoom_user_account_enc SET firstName ="'+firstName+'"'
if debug : print(keystr)
db.execute(keystr)

#lastName
usr_acc=db.execute('select lastName FROM zoom_user_account_enc').fetchall()
if debug : print(usr_acc)
lastName = decField(usr_acc[0][0])
if debug : print("lastName: "+lastName)
keystr='UPDATE zoom_user_account_enc SET lastName ="'+lastName+'"'
if debug : print(keystr)
db.execute(keystr)

#commit and close
db.commit()
db.close()
