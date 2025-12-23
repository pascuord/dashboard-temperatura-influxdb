import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logger():
    """
    Configura el sistema de logging con salida dual:
    - Consola: INFO y superiores
    - Archivo: ERROR y superiores
    """
    # Crear directorio de logs si no existe
    log_dir = '/app/logs'
    os.makedirs(log_dir, exist_ok=True)
    
    # Configurar el logger raíz
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)  # Capturar todos los niveles
    
    # Evitar duplicación de handlers
    if logger.handlers:
        return logger
    
    # Formato detallado para logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Handler para CONSOLA (INFO y superiores)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # Handler para ARCHIVO (ERROR y superiores)
    # RotatingFileHandler para evitar archivos gigantes
    file_handler = RotatingFileHandler(
        f'{log_dir}/error.log',
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5  # Mantener 5 archivos de respaldo
    )
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Handler adicional para app.log (todos los niveles)
    app_handler = RotatingFileHandler(
        f'{log_dir}/app.log',
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=3
    )
    app_handler.setLevel(logging.INFO)
    app_handler.setFormatter(formatter)
    logger.addHandler(app_handler)
    
    return logger

# Crear instancia global del logger
logger = setup_logger()

