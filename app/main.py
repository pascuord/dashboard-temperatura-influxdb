import threading
from app import create_app
from app.db import init_db
from app.services import escribir_datos_temperatura
from app.logger import logger

def main():
    # Inicializar base de datos
    logger.info("=== Iniciando aplicación ===")
    init_db()
    
    # Crear aplicación Flask
    app = create_app()
    
    # Iniciar hilo de escritura de datos en segundo plano
    hilo_escritura = threading.Thread(target=escribir_datos_temperatura, daemon=True)
    hilo_escritura.start()
    logger.info("Hilo de escritura de datos iniciado")
    
    # Iniciar servidor Flask
    logger.info("Iniciando servidor Flask en 0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)

if __name__ == '__main__':
    main()

