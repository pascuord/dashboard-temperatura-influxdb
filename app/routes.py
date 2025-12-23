from flask import Blueprint, jsonify, request
from app.db import get_query_api, get_client
from app.config import Config
from app.logger import logger

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/datos', methods=['GET'])
def obtener_datos():
    """Endpoint para obtener puntos de temperatura en un rango de tiempo"""
    query_api = get_query_api()
    if not query_api:
        logger.warning("Intento de acceso a /api/datos sin conexión a InfluxDB")
        return jsonify({"error": "No hay conexión a InfluxDB"}), 503
    
    # Obtener parámetro de rango (por defecto: 1h)
    rango = request.args.get('rango', '1h')
    logger.info(f"Solicitados datos con rango: {rango}")
    
    # Validar que el rango sea uno de los permitidos
    rangos_permitidos = ['1h', '6h', '24h']
    if rango not in rangos_permitidos:
        logger.warning(f"Rango inválido solicitado: {rango}")
        return jsonify({"error": f"Rango inválido. Use: {', '.join(rangos_permitidos)}"}), 400
    
    try:
        # Usar el rango en la query y aumentar límite a 100
        query = f'''
        from(bucket: "{Config.INFLUXDB_BUCKET}")
            |> range(start: -{rango})
            |> filter(fn: (r) => r["_measurement"] == "temperatura")
            |> filter(fn: (r) => r["_field"] == "value")
            |> sort(columns: ["_time"], desc: true)
            |> limit(n: 100)
        '''
        
        result = query_api.query(org=Config.INFLUXDB_ORG, query=query)
        
        datos = []
        for table in result:
            for record in table.records:
                datos.append({
                    "tiempo": record.get_time().isoformat(),
                    "temperatura": record.get_value()
                })
        
        datos.reverse()
        logger.info(f"Devolviendo {len(datos)} puntos de datos")
        
        return jsonify({
            "datos": datos,
            "total": len(datos)
        }), 200
        
    except Exception as e:
        logger.error(f"Error al consultar datos: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@api_bp.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    client = get_client()
    return jsonify({
        "status": "ok",
        "influxdb_conectado": client is not None
    }), 200

@api_bp.route('/api/test-error', methods=['GET'])
def test_error():
    """Endpoint de prueba para forzar un error y verificar logging"""
    logger.warning("Endpoint de prueba /api/test-error invocado")
    try:
        # Forzar un error intencional
        resultado = 1 / 0  # ZeroDivisionError
    except Exception as e:
        logger.error(f"Error forzado para prueba: {e}", exc_info=True)
        return jsonify({
            "mensaje": "Error forzado registrado exitosamente",
            "error": str(e),
            "nota": "Revisa /app/logs/error.log en el contenedor"
        }), 500

