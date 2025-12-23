# Dashboard de Temperatura con InfluxDB

Sistema de monitoreo de temperatura en tiempo real con backend Flask, base de datos InfluxDB v2 y frontend React.

## 🚀 Características

- **Backend Flask**: API REST para escritura y consulta de datos
- **InfluxDB v2**: Base de datos de series temporales para almacenamiento eficiente
- **Frontend React**: Dashboard interactivo con gráficos en tiempo real
- **Docker Compose**: Despliegue completo con un solo comando
- **Logging profesional**: Sistema de logs con rotación y persistencia
- **Filtros de tiempo**: Visualización de datos por 1h, 6h o 24h

## 📊 Arquitectura

```
proyecto_dia1/
├── app/                    # Backend Flask
│   ├── __init__.py        # Factory pattern
│   ├── config.py          # Configuración centralizada
│   ├── db.py              # Cliente InfluxDB
│   ├── logger.py          # Sistema de logging
│   ├── main.py            # Punto de entrada
│   ├── routes.py          # Endpoints API
│   └── services.py        # Lógica de negocio
├── frontend/              # Frontend React + Vite
│   ├── src/
│   │   ├── App.jsx        # Dashboard principal
│   │   └── main.jsx
│   └── Dockerfile
├── docker-compose.yml     # Orquestación de servicios
├── Dockerfile             # Imagen del backend
└── requirements.txt       # Dependencias Python
```

## 🛠️ Tecnologías

- **Backend**: Python 3.11, Flask 3.0, InfluxDB Client, Flask-CORS
- **Frontend**: React 18, Vite 7, Chart.js, react-chartjs-2, Axios
- **Base de datos**: InfluxDB 2.7
- **Contenedores**: Docker, Docker Compose V2

## 📦 Instalación y Uso

### Prerrequisitos

- Docker y Docker Compose V2 instalados
- Puertos 5000, 5173 y 8086 disponibles

### Iniciar el sistema

```bash
# Clonar el repositorio
git clone <tu-repo-url>
cd proyecto_dia1

# Levantar todos los servicios
docker compose up -d --build

# Ver logs
docker compose logs -f
```

### Acceder a los servicios

- **Frontend (Dashboard)**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **InfluxDB UI**: http://localhost:8086

### Detener el sistema

```bash
docker compose down
```

## 🔧 Configuración

Variables de entorno configurables en `docker-compose.yml`:

```yaml
INFLUXDB_URL: http://influxdb:8086
INFLUXDB_TOKEN: my-token
INFLUXDB_ORG: my-org
INFLUXDB_BUCKET: my-bucket
INTERVALO_SEGUNDOS: 2  # Intervalo de escritura de datos
```

## 📡 Endpoints API

### `GET /api/datos`
Obtiene datos de temperatura con filtro de tiempo.

**Query params:**
- `rango` (opcional): `1h`, `6h`, `24h` (default: `1h`)

**Respuesta:**
```json
{
  "datos": [
    {
      "tiempo": "2025-12-23T18:05:00Z",
      "temperatura": 45.32
    }
  ],
  "total": 100
}
```

### `GET /health`
Health check del servicio.

### `GET /api/test-error`
Endpoint de prueba para verificar el sistema de logging.

## 📝 Logging

Los logs se almacenan en:
- `/app/logs/app.log`: Logs generales (INFO+)
- `/app/logs/error.log`: Solo errores (ERROR+)
- Consola: INFO y superiores

Los logs persisten en un volumen Docker para no perderse al reiniciar.

## 🎨 Características del Dashboard

- **Gráfico de línea** con Chart.js mostrando evolución temporal
- **Actualización automática** cada 2 segundos
- **Filtros de tiempo**: Botones para ver 1h, 6h o 24h
- **Interfaz moderna** con gradientes y efectos hover
- **Diseño responsive** y centrado

## 🧪 Generación de Datos

El sistema genera temperaturas simuladas con:
- **Rango**: 0-100°C
- **Cambio gradual**: ±10°C por lectura (curvas suaves)
- **Frecuencia**: Cada 2 segundos (configurable)

## 📄 Licencia

MIT

## 👤 Autor

Pascual Ordiñana Soler - pascuord
