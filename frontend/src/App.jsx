import { useState, useEffect } from 'react'
import axios from 'axios'
import { Line } from 'react-chartjs-2'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import './App.css'

// Registrar componentes de Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

function App() {
  const [datos, setDatos] = useState([])
  const [ultimaActualizacion, setUltimaActualizacion] = useState(null)
  const [error, setError] = useState(null)
  const [rangoActivo, setRangoActivo] = useState('1h')

  // URL de la API (funciona en Docker y desarrollo local)
  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

  // Función para manejar cambio de rango
  const cambiarRango = (nuevoRango) => {
    setRangoActivo(nuevoRango)
  }

  // Efecto para cargar datos cada 2 segundos
  useEffect(() => {
    // Función para obtener datos de la API
    const obtenerDatos = async () => {
      try {
        const response = await axios.get(`${API_URL}/api/datos?rango=${rangoActivo}`)
        setDatos(response.data.datos)
        setUltimaActualizacion(new Date().toLocaleTimeString())
        setError(null)
      } catch (err) {
        console.error('Error al obtener datos:', err)
        setError('No se pudo conectar con el backend')
      }
    }

    // Cargar datos inmediatamente
    obtenerDatos()

    // Configurar intervalo de actualización
    const intervalo = setInterval(obtenerDatos, 2000)

    // Limpiar intervalo al desmontar
    return () => clearInterval(intervalo)
  }, [API_URL, rangoActivo])

  // Preparar datos para el gráfico
  const chartData = {
    labels: datos.map(d => {
      const fecha = new Date(d.tiempo)
      return fecha.toLocaleTimeString()
    }),
    datasets: [
      {
        label: 'Temperatura (°C)',
        data: datos.map(d => d.temperatura),
        borderColor: 'rgb(75, 192, 192)',
        backgroundColor: 'rgba(75, 192, 192, 0.2)',
        fill: true,
        tension: 0.4,
        borderWidth: 2,
        pointRadius: 3,
        pointHoverRadius: 5
      }
    ]
  }

  // Opciones del gráfico
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          font: {
            size: 14
          }
        }
      },
      title: {
        display: true,
        text: 'Monitor de Temperatura en Tiempo Real',
        font: {
          size: 20,
          weight: 'bold'
        }
      },
      tooltip: {
        mode: 'index',
        intersect: false,
      }
    },
    scales: {
      y: {
        beginAtZero: false,
        title: {
          display: true,
          text: 'Temperatura (°C)',
          font: {
            size: 14
          }
        }
      },
      x: {
        title: {
          display: true,
          text: 'Tiempo',
          font: {
            size: 14
          }
        }
      }
    }
  }

  return (
    <div style={{
      padding: '20px',
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center'
    }}>
      <div style={{
        maxWidth: '1200px',
        width: '100%',
        background: 'white',
        borderRadius: '15px',
        padding: '30px',
        boxShadow: '0 10px 30px rgba(0,0,0,0.2)'
      }}>
        <h1 style={{
          textAlign: 'center',
          color: '#333',
          marginBottom: '10px',
          fontSize: '2.5em'
        }}>
          📊 Dashboard de Temperatura
        </h1>

        {error ? (
          <div style={{
            background: '#fee',
            color: '#c33',
            padding: '15px',
            borderRadius: '8px',
            textAlign: 'center',
            marginBottom: '20px',
            border: '1px solid #fcc'
          }}>
            ⚠️ {error}
          </div>
        ) : (
          <div style={{
            textAlign: 'center',
            color: '#666',
            marginBottom: '20px',
            fontSize: '0.9em'
          }}>
            <span style={{
              background: '#e8f5e9',
              padding: '5px 15px',
              borderRadius: '20px',
              display: 'inline-block'
            }}>
              🟢 Conectado | Última actualización: {ultimaActualizacion}
            </span>
          </div>
        )}

        {/* Botones de filtro de tiempo */}
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          gap: '10px',
          marginBottom: '20px'
        }}>
          {['1h', '6h', '24h'].map((rango) => (
            <button
              key={rango}
              onClick={() => cambiarRango(rango)}
              style={{
                padding: '10px 25px',
                fontSize: '1em',
                fontWeight: rangoActivo === rango ? 'bold' : 'normal',
                backgroundColor: rangoActivo === rango ? '#667eea' : '#f0f0f0',
                color: rangoActivo === rango ? 'white' : '#333',
                border: rangoActivo === rango ? '2px solid #5568d3' : '2px solid #ddd',
                borderRadius: '8px',
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                boxShadow: rangoActivo === rango ? '0 4px 8px rgba(102, 126, 234, 0.3)' : 'none'
              }}
              onMouseEnter={(e) => {
                if (rangoActivo !== rango) {
                  e.target.style.backgroundColor = '#e8e8e8'
                  e.target.style.borderColor = '#bbb'
                }
              }}
              onMouseLeave={(e) => {
                if (rangoActivo !== rango) {
                  e.target.style.backgroundColor = '#f0f0f0'
                  e.target.style.borderColor = '#ddd'
                }
              }}
            >
              {rango === '1h' ? 'Última hora' : rango === '6h' ? 'Últimas 6 horas' : 'Últimas 24 horas'}
            </button>
          ))}
        </div>

        <div style={{
          background: '#f9f9f9',
          borderRadius: '10px',
          padding: '20px',
          height: '500px'
        }}>
          {datos.length > 0 ? (
            <Line data={chartData} options={chartOptions} />
          ) : (
            <div style={{
              display: 'flex',
              justifyContent: 'center',
              alignItems: 'center',
              height: '100%',
              color: '#999'
            }}>
              <p>Cargando datos...</p>
            </div>
          )}
        </div>

        <div style={{
          marginTop: '20px',
          display: 'flex',
          justifyContent: 'space-around',
          textAlign: 'center'
        }}>
          <div style={{
            background: '#e3f2fd',
            padding: '15px 25px',
            borderRadius: '10px',
            flex: 1,
            margin: '0 10px'
          }}>
            <div style={{ fontSize: '0.9em', color: '#666' }}>Puntos de datos</div>
            <div style={{ fontSize: '2em', fontWeight: 'bold', color: '#1976d2' }}>
              {datos.length}
            </div>
          </div>
          <div style={{
            background: '#fff3e0',
            padding: '15px 25px',
            borderRadius: '10px',
            flex: 1,
            margin: '0 10px'
          }}>
            <div style={{ fontSize: '0.9em', color: '#666' }}>Temperatura actual</div>
            <div style={{ fontSize: '2em', fontWeight: 'bold', color: '#f57c00' }}>
              {datos.length > 0 ? `${datos[datos.length - 1].temperatura}°C` : '--'}
            </div>
          </div>
          <div style={{
            background: '#fce4ec',
            padding: '15px 25px',
            borderRadius: '10px',
            flex: 1,
            margin: '0 10px'
          }}>
            <div style={{ fontSize: '0.9em', color: '#666' }}>Temperatura promedio</div>
            <div style={{ fontSize: '2em', fontWeight: 'bold', color: '#c2185b' }}>
              {datos.length > 0 
                ? `${(datos.reduce((sum, d) => sum + d.temperatura, 0) / datos.length).toFixed(2)}°C`
                : '--'
              }
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
