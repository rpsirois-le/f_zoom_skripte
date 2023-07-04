if os.path.exists(accountDBPath+"/dec/"+accountDBPath+".idx.db"):
    os.remove(accountDBPath+"/dec/"+accountDBPath+".idx.db")
    print("old zoom.us.idx.db removed")
else:
    print("The file zoom.us.idx.db does not exist, creating new")
db = sqlcipher.connect(accountDBPath+'/'+accountDBPath+'.idx.encks.db')
db.execute(keystr)
db.execute('PRAGMA kdf_iter = "4000"')
db.execute('PRAGMA cipher_page_size = 1024')
dbstring='ATTACH DATABASE "'+accountDBPath+'/dec/'+accountDBPath+'.idx.db" AS zoom KEY ""'
db.execute(dbstring)
db.execute('SELECT sqlcipher_export("zoom")')
db.execute('DETACH DATABASE zoom')
db.close()
