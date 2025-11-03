# Dashboard de Análisis de Películas - MongoDB Atlas

Proyecto de Big Data que visualiza análisis de ratings de películas desde MongoDB Atlas.

## 📋 Descripción del Proyecto

Este proyecto implementa una solución completa de análisis de datos de películas que incluye:

1. **Carga de datos**: Script Python para cargar datos de `title.ratings.tsv` a MongoDB Atlas
2. **API REST**: Backend en Flask que expone endpoints para análisis de datos
3. **Dashboard Web**: Aplicación web local con visualizaciones interactivas usando Chart.js

### Análisis de Negocio Implementados

- **Distribución de Calificaciones**: Muestra cómo se distribuyen los ratings en el catálogo
- **Análisis de Engagement**: Relación entre popularidad (votos) y cantidad de títulos
- **Calidad vs Popularidad**: Identifica patrones entre calidad percibida y engagement de audiencia
- **KPIs del Catálogo**: Métricas clave como películas de alta calidad, populares, etc.

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- Conexión a Internet (para MongoDB Atlas)
- pip (gestor de paquetes de Python)

### ⚠️ Importante para Python 3.13 en macOS

Si tienes Python 3.13 instalado vía Homebrew, verás un error de "externally-managed-environment".

**Solución simple:**
```bash
bash quick_start.sh
```

Este script crea automáticamente un entorno virtual y configura todo. Ver `SOLUCION_PYTHON_3.13.md` para más detalles.

### Paso 1: Instalar Dependencias

**Opción A - Con entorno virtual (Python 3.13 macOS):**
```bash
bash setup_venv.sh
```

**Opción B - Instalación directa (otras versiones):**
```bash
pip install -r requirements.txt
```

O instalar manualmente:
```bash
pip install Flask==3.0.0 pymongo==4.6.0 dnspython==2.4.2
```

## 📊 Uso

### 1. Cargar Datos a MongoDB

**Importante**: El cluster tiene espacio limitado, por defecto se cargan solo 100,000 registros.

```bash
# Cargar 100,000 registros (recomendado)
python load_data.py

# Cargar un número específico de registros
python load_data.py 50000

# Cargar todos los registros (⚠️ ~1.6 millones - verificar espacio)
python load_data.py all
```

El script:
- Limpia la colección existente
- Carga datos en lotes para optimizar memoria
- Crea índices automáticamente
- Muestra estadísticas al finalizar

**Salida esperada:**
```
Conectando a MongoDB Atlas...
Limpiando colección 'ratings'...
Cargando datos desde title.ratings.tsv...
Insertados 1000 registros...
Insertados 2000 registros...
...
✓ Carga completada: 100000 registros insertados

--- Estadísticas ---
Total de documentos: 100000
Rating promedio: 6.45
Rating máximo: 10.00
Rating mínimo: 1.00
Total de votos: 15,234,567
```

### 2. Iniciar la Aplicación Web

```bash
python app.py
```

La aplicación estará disponible en: **http://localhost:5000**

**Salida esperada:**
```
Iniciando aplicación en http://localhost:5000
 * Running on http://0.0.0.0:5000
 * Debug mode: on
```

### 3. Visualizar el Dashboard

1. Abre tu navegador en `http://localhost:5000`
2. El dashboard cargará automáticamente las visualizaciones
3. Podrás ver:
   - 4 métricas principales en tarjetas
   - 3 gráficas interactivas con análisis de negocio

## 🎯 Estructura del Proyecto

```
mongo_atlas_graficas/
├── load_data.py          # Script para cargar datos a MongoDB
├── app.py                # Aplicación Flask con API
├── templates/
│   └── index.html        # Dashboard con visualizaciones
├── requirements.txt      # Dependencias del proyecto
├── README.md            # Este archivo
├── title.ratings.tsv    # Datos fuente (no incluir en git)
└── MongoDBRocketSpace.docx  # Documento con requisitos
```

## 📈 APIs Disponibles

La aplicación expone los siguientes endpoints:

### `GET /api/rating-distribution`
Distribuci\u00f3n de películas por rangos de rating.

**Respuesta:**
```json
{
  "labels": ["0-2", "2-4", "4-6", "6-8", "8-10"],
  "counts": [1234, 5678, 45000, 38000, 10088],
  "avgVotes": [150.5, 320.8, 890.2, 2300.5, 15000.3]
}
```

### `GET /api/top-rated-popular`
Top 20 películas mejor calificadas con alta popularidad (≥10,000 votos, rating ≥7.0).

**Respuesta:**
```json
{
  "movies": [
    {
      "tconst": "tt0111161",
      "averageRating": 9.3,
      "numVotes": 2500000
    }
  ]
}
```

### `GET /api/votes-analysis`
Análisis de engagement por rangos de votos.

**Respuesta:**
```json
{
  "labels": ["0-100", "100-1K", "1K-10K", "10K-100K", "100K-1M"],
  "counts": [50000, 30000, 15000, 4000, 900],
  "avgRatings": [6.2, 6.5, 6.8, 7.2, 7.8]
}
```

### `GET /api/quality-metrics`
KPIs generales del catálogo.

**Respuesta:**
```json
{
  "totalMovies": 100000,
  "avgRating": 6.45,
  "avgVotes": 1523.45,
  "totalVotes": 152345678,
  "highQuality": 10088,
  "popular": 8765,
  "lowRated": 5432
}
```

## 🔧 Configuración

### Cambiar Conexión a MongoDB

Si necesitas cambiar la conexión, edita en ambos archivos (`load_data.py` y `app.py`):

```python
MONGO_URI = "tu_connection_string_aqui"
DATABASE_NAME = "tu_base_de_datos"
COLLECTION_NAME = "tu_coleccion"
```

### Cambiar Puerto de la Aplicación

En `app.py`, modifica:

```python
app.run(debug=True, host='0.0.0.0', port=5000)  # Cambia 5000 por el puerto deseado
```

## 🎨 Personalizar Visualizaciones

Las gráficas se crean con **Chart.js** en `templates/index.html`. Puedes modificar:

- Colores: En el objeto `colors` del JavaScript
- Tipos de gráfica: Cambia `type: 'bar'` por `'line'`, `'pie'`, `'doughnut'`, etc.
- Opciones: Modifica el objeto `options` de cada gráfica

## ❗ Solución de Problemas

### Error de conexión a MongoDB
```
pymongo.errors.ConfigurationError: Invalid URI scheme
```
**Solución**: Verifica que el connection string sea correcto y tenga el prefijo `mongodb+srv://`

### Error: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'pymongo'
```
**Solución**: Instala las dependencias con `pip install -r requirements.txt`

### La aplicación no carga datos
**Solución**: 
1. Verifica que hayas ejecutado `load_data.py` primero
2. Confirma que la base de datos tenga registros
3. Revisa la consola de la aplicación para errores

### Puerto 5000 en uso
```
OSError: [Errno 48] Address already in use
```
**Solución**: Cambia el puerto en `app.py` o mata el proceso:
```bash
lsof -ti:5000 | xargs kill
```

## 📝 Notas Importantes

- **Espacio limitado**: El cluster de MongoDB Atlas tiene espacio limitado. Usa 100,000 registros por defecto.
- **Datos de ejemplo**: Los datos son de IMDb (title.ratings.tsv)
- **Modo desarrollo**: La aplicación corre en modo debug, no usar en producción
- **Índices**: Se crean automáticamente en `averageRating` y `numVotes` para optimizar consultas

## 🎓 Entregables del Proyecto

1. ✅ Código fuente completo (`load_data.py`, `app.py`, `templates/index.html`)
2. ✅ Visualizaciones de análisis de negocio (3 gráficas + métricas)
3. ✅ Datos cargados en MongoDB Atlas
4. ✅ Aplicación funcional corriendo localmente
5. ✅ README con instrucciones completas

## 👤 Autor

Proyecto desarrollado para el curso de Big Data - MongoDB & Data Visualization

---

**¡Listo para usar!** 🚀

Para comenzar:
```bash
pip install -r requirements.txt
python load_data.py
python app.py
```

# bigdata_mongoatlasgrafica
