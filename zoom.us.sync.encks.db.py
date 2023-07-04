if os.path.exists(accountDBPath+"/dec/"+accountDBPath+".sync.db"):
    os.remove(accountDBPath+"/dec/"+accountDBPath+".sync.db")
    print("old zoom.us.sync.db removed")
else:
    print("The file zoom.us.sync.db does not exist, creating new")
db = sqlcipher.connect(accountDBPath+'/'+accountDBPath+'.sync.encks.db')
db.execute(keystr)
db.execute('PRAGMA kdf_iter = "4000"')
db.execute('PRAGMA cipher_page_size = 1024')
dbstring='ATTACH DATABASE "'+accountDBPath+'/dec/'+accountDBPath+'.sync.db" AS zoom KEY ""'
db.execute(dbstring)
db.execute('SELECT sqlcipher_export("zoom")')
db.execute('DETACH DATABASE zoom')
db.close()
