import os, requests
from influxdb import InfluxDBClient
from dotenv import load_dotenv

load_dotenv()

cid = os.getenv("FORMLABS_CLIENT_ID")
secret = os.getenv("FORMLABS_CLIENT_SECRET")
r = requests.post("https://api.formlabs.com/oauth/token/", data={
    "grant_type": "client_credentials",
    "client_id": cid,
    "client_secret": secret
})
token = r.json().get("access_token")
resp = requests.get("https://api.formlabs.com/v1/printers/", headers={"Authorization": f"Bearer {token}"})
printers = resp.json()

client = InfluxDBClient(host=os.getenv("INFLUX_HOST"), port=int(os.getenv("INFLUX_PORT")), database=os.getenv("INFLUX_DB"))

data = []
for p in printers:
    data.append({
        "measurement": "formlabs_status",
        "tags": {
            "name": p.get("name", "unknown"),
            "model": p.get("model", "Form")
        },
        "fields": {
            "status": p.get("status", "offline"),
            "resin": p.get("resin_type", "unknown") or "unknown"
        }
    })
client.write_points(data)
print(f"Pushed {len(data)} Formlabs printer statuses.")
