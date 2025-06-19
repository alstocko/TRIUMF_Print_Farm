import os, requests
from influxdb import InfluxDBClient
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("PRUSA_API_TOKEN")
headers = {"Authorization": token}
resp = requests.get("https://connect.prusa3d.com/api/printers", headers=headers)
printers = resp.json()

client = InfluxDBClient(host=os.getenv("INFLUX_HOST"), port=int(os.getenv("INFLUX_PORT")), database=os.getenv("INFLUX_DB"))

data = []
for p in printers:
    data.append({
        "measurement": "prusa_status",
        "tags": {
            "name": p.get("name", "unknown")
        },
        "fields": {
            "state": str(p.get("state", "offline")),
            "model": p.get("printer_type", "unknown")
        }
    })
client.write_points(data)
print(f"Pushed {len(data)} printer statuses.")
