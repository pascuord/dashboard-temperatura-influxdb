import time
import random
from influxdb_client import Point, WritePrecision
from app.db import get_write_api
from app.config import Config
from app.logger import logger

def escribir_datos_temperatura():
    """Función que escribe datos de temperatura en segundo plano"""
    logger.info("Iniciando hilo de escritura de datos de temperatura")
    write_api = get_write_api()
    
    # Temperatura inicial en el rango ampliado (0-100)
    temperature = round(random.uniform(40, 60), 2)
    
    while True:
        # Cambio gradual: +/- 10 grados respecto a la temperatura anterior
        cambio = random.uniform(-10, 10)
        temperature = round(temperature + cambio, 2)
        
        # Mantener temperatura dentro del rango 0-100
        if temperature > 100:
            temperature = 100
        elif temperature < 0:
            temperature = 0
        
        point = Point("temperatura").field("value", temperature).time(time.time_ns(), WritePrecision.NS)
        try:
            if write_api:
                write_api.write(bucket=Config.INFLUXDB_BUCKET, 
                               org=Config.INFLUXDB_ORG, 
                               record=point)
                logger.info(f"Temperatura enviada: {temperature}°C")
            else:
                logger.warning("write_api no está disponible")
        except Exception as e:
            logger.error(f"Error al enviar datos a InfluxDB: {e}", exc_info=True)
        time.sleep(Config.INTERVALO_SEGUNDOS)

