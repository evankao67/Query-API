import json, requests, psycopg2
APITOKEN = "LNiex3PKQZc6oijpR4H1L9Nh3q0gjbrjuMXhegZBJZw="
SERVICE = "https://api.cresclab.com/openapi/v1/member/"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + APITOKEN
}

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
        PARAM = input("請輸入客戶之member id:")
    except:
        conn.commit()
        conn.close()
        exit()
    try:
        tag_list=""
        res = requests.get(SERVICE + "?customer_id=" + PARAM, headers = HEADERS).json()
        #print(res)
        if len(res["results"]) == 0:
                continue
        for result in res["results"][0]["tags"]:
            tag_list = tag_list+result+", "
        
        sql = """INSERT INTO query_ (lm, line_id, tags) VALUES (%(lm)s, %(line_id)s, %(tags)s)"""
        params = {
             'lm':res["results"][0]["customer_id"],
             'line_id':res["results"][0]["line_uid"],
             'tags':tag_list
        }
        cursor.execute(sql,params)
    except:
        print("error")
