from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from app.config import Config
from app.logger import logger

_client = None
_write_api = None
_query_api = None

def init_db():
    global _client, _write_api, _query_api
    try:
        _client = InfluxDBClient(url=Config.INFLUXDB_URL, 
                                 token=Config.INFLUXDB_TOKEN, 
                                 org=Config.INFLUXDB_ORG)
        _write_api = _client.write_api(write_options=SYNCHRONOUS)
        _query_api = _client.query_api()
        logger.info(f"✓ Conectado a InfluxDB en {Config.INFLUXDB_URL}")
    except Exception as e:
        logger.error(f"Error al conectar a InfluxDB: {e}", exc_info=True)

def get_client():
    return _client

def get_write_api():
    return _write_api

def get_query_api():
    return _query_api

