if os.path.exists(accountDBPath+"/dec/"+accountDBPath+".asyn.db"):
    os.remove(accountDBPath+"/dec/"+accountDBPath+".asyn.db")
    print("old zoom.us.asyn.db removed")
else:
    print("The file zoom.us.asyn.db does not exist, creating new")
db = sqlcipher.connect(accountDBPath+'/'+accountDBPath+'.asyn.encks.db')
db.execute(keystr)
db.execute('PRAGMA kdf_iter = "4000"')
db.execute('PRAGMA cipher_page_size = 1024')
dbstring='ATTACH DATABASE "'+accountDBPath+'/dec/'+accountDBPath+'.asyn.db" AS zoom KEY ""'
db.execute(dbstring)
db.execute('SELECT sqlcipher_export("zoom")')
db.execute('DETACH DATABASE zoom')
db.close()
