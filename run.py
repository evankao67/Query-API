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

#Query Function
def generate_apis(param):
    return [
        SERVICE + "?line_uid=" + param,
        SERVICE + "?email=" + param,
        SERVICE + "?mobile=" + param,
    ]

#主程式 call api 的tags 到DB
while True:
    try:
        PARAM = input("請輸入line_uid、email或phone來取得該客戶的tags:")
    except:
        conn.commit()
        conn.close()
        exit()
    
    for api in generate_apis(PARAM):
        try:
            tag_list=""
            res = requests.get(api, headers = HEADERS).json()
            if len(res["results"]) == 0:
                continue
            for result in res["results"][0]["tags"]:
                tag_list = tag_list+result+", "
            
            sql =f"UPDATE brand_line_id SET tags = '{tag_list}' WHERE lineid = '{PARAM}' OR phone = '{PARAM}' OR email = '{PARAM}'"
            cursor.execute(sql)
        except:
            print("error")

        
