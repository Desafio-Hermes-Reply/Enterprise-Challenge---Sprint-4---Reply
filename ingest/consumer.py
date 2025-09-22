import json, psycopg2
import paho.mqtt.client as mqtt
from jsonschema import validate, ValidationError
import yaml, time

# Config
cfg = yaml.safe_load(open("ingest/config.yaml"))
dsn = cfg["db"]["dsn"]

# Schema
import pathlib
schema = json.load(open(pathlib.Path("ingest/schema/v1.json")))

# DB
conn = psycopg2.connect(dsn)
cur = conn.cursor()

def insert(data):
    cur.execute("""
        INSERT INTO sensor_readings(sensor_id, ts, type, value)
        VALUES (%s, to_timestamp(%s/1000.0), %s, %s)
        ON CONFLICT DO NOTHING
    """, (data["sensor_id"], data["timestamp_ms"], data["type"], data["value"]))
    conn.commit()

# Métricas simples
metrics = {"received": 0, "saved": 0, "failed": 0}

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        validate(data, schema)
        insert(data)
        metrics["saved"] += 1
    except (json.JSONDecodeError, ValidationError):
        metrics["failed"] += 1
    metrics["received"] += 1
    print(metrics)

client = mqtt.Client()
client.connect(cfg["mqtt"]["host"], cfg["mqtt"]["port"], 60)
client.subscribe(cfg["mqtt"]["topic"], qos=1)
client.on_message = on_message

print("Consumer POC rodando...")
client.loop_forever()
