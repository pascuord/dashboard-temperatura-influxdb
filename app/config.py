import os

class Config:
    INFLUXDB_URL = os.getenv("INFLUXDB_URL", "http://localhost:8086")
    INFLUXDB_TOKEN = os.getenv("INFLUXDB_TOKEN", "my-token")
    INFLUXDB_ORG = os.getenv("INFLUXDB_ORG", "my-org")
    INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET", "my-bucket")
    INTERVALO_SEGUNDOS = int(os.getenv("INTERVALO_SEGUNDOS", "5"))

