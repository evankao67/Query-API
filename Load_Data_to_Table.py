import json, requests, psycopg2
APITOKEN = "LNiex3PKQZc6oijpR4H1L9Nh3q0gjbrjuMXhegZBJZw="
SERVICE = "https://api.cresclab.com/openapi/v1/member/"
HEADERS = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + APITOKEN
}
DB_CONFIG = {}

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

#把整張表（除了tags）讀進DB
try:
    tmp = requests.get(SERVICE, headers = HEADERS).json()
    sql ="""INSERT INTO brand_line_id (lineid, name_, phone, email, status_, gender, birthday, updated_at, created_at, member_id) VALUES (%(lineid)s, %(name_)s, %(phone)s, %(email)s, %(status_)s, %(gender)s, %(birthday)s, %(updated_at)s, %(created_at)s, %(member_id)s)"""
    for i in range(len(tmp["results"])):
        params = {'lineid':tmp["results"][i]["line_uid"],
                  'name_':tmp["results"][i]["line_display_name"],
                  'phone':tmp["results"][i]["mobile"],
                  'email':tmp["results"][i]["email"],
                  'status_':tmp["results"][i]["status"],
                  'gender':tmp["results"][i]["gender"],
                  'birthday':tmp["results"][i]["birthday"],
                  'updated_at':tmp["results"][i]["updated_at"],
                  'created_at':tmp["results"][i]["created_at"],
                  'member_id':tmp["results"][i]["customer_id"]
                  }
        cursor.execute(sql,params)
except:
    print("error")

conn.commit()
conn.close()
