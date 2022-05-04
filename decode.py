from numpy import character
import json, requests, psycopg2
import requests, base64

try:
    with open('config.json', 'r') as f:
        DB_CONFIG = json.loads(f.read())
except: 
    DB_CONFIG = {
        "database": "postgres",
        "user": "evan",
        "password": "206803",
        "host": "127.0.0.1",
        "port": "5432"
    }

conn = psycopg2.connect(database=DB_CONFIG["database"], user=DB_CONFIG["user"], password=DB_CONFIG["password"], host=DB_CONFIG["host"], port=DB_CONFIG["port"])
cursor = conn.cursor()


while True:
    try:
       url = input("input a valid url: ")
    except:
        conn.commit()
        conn.close()
        exit()
    
    Url = requests.utils.unquote(url)
    tmp = base64.b64decode(Url + '=' * (-len(Url) % 4))
    ans = ""
    for i in range(len(tmp)):
        if tmp[i] > 47 and tmp[i] < 58:
            ans+=chr(tmp[i]) 
    sql = """INSERT INTO decode (clid, memberid) VALUES (%(clid)s, %(memberid)s)"""
    params = {
        'clid':url,
        'memberid':ans
    }
    cursor.execute(sql, params)
