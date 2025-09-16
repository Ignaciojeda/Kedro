# 🏀 Análisis de Datos NBA con Kedro

## 📋 Descripción del Proyecto
Este proyecto analiza datos de la **NBA** para identificar patrones de rendimiento de equipos, especialmente su desempeño como **local** vs. **visitante**.  
Se utiliza el framework **Kedro** para crear pipelines reproducibles y modulares de procesamiento de datos.

---

## 🎯 Objetivos Principales
- 📌 Identificar qué equipos son mejores jugando en casa  
- 📌 Analizar qué equipos son peores como visitantes  
- 📌 Estudiar patrones ofensivos y defensivos  
- 📌 Crear pipelines modulares y reproducibles  

---

## 📊 Datasets Utilizados
El proyecto utiliza **3 datasets principales de Kaggle (NBA Games)**:

| Dataset | Descripción |
|--------|-------------|
| `games.csv` | Resultados y estadísticas de partidos |
| `games_details.csv` | Estadísticas por jugador por partido |
| `teams.csv` | Información de los equipos |

**Fuente:** [Kaggle - NBA Games Dataset](https://www.kaggle.com/datasets/nathanlauga/nba-games?select=games.csv)

---

## 🚀 Instalación y Configuración

### 🔑 Prerrequisitos
- Python **3.8+**
- `pip`
- `virtualenv` (recomendado)

### 1️⃣ Clonar y Configurar el Proyecto

```bash
# Clonar repositorio
git clone <url_del_repositorio>
cd nba-analysis

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Linux / Mac
source venv/bin/activate
# Windows
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
2️⃣ Configurar los Datos
bash
Copiar código
# Crear estructura de carpetas de datos
mkdir -p data/01_raw
📥 Descargar datasets de Kaggle y colocarlos en:

data/01_raw/games.csv

data/01_raw/games_details.csv

data/01_raw/teams.csv

3️⃣ Configurar Kedro
bash
Copiar código
# Verificar información del proyecto
kedro info
🏃‍♂️ Ejecución del Proyecto
Ejecutar el Pipeline Completo
bash
Copiar código
kedro run
Ejecutar Pipelines Específicos
bash
Copiar código
# Solo data engineering
kedro run --pipeline=data_engineering

# Solo un nodo específico
kedro run --node=clean_games_data_node
Visualizar el Pipeline
bash
Copiar código
kedro viz
# Abrir en navegador: http://127.0.0.1:4141
Trabajar con Notebooks
bash
Copiar código
# Abrir Jupyter con contexto de Kedro
kedro jupyter notebook

# Abrir notebook específico
kedro jupyter notebook --notebook-path notebooks/03_data_preparation.ipynb
📝 Notebooks Disponibles
Notebook	Contenido
01_business_understanding.ipynb	Definición de objetivos, preguntas de negocio, plan del proyecto
02_data_understanding.ipynb	EDA, validación de calidad de datos, visualizaciones iniciales
03_data_preparation.ipynb	Limpieza, feature engineering, preparación para modelado

🔧 Comandos Útiles
bash
Copiar código
# Ver información del proyecto
kedro info

# Listar datasets disponibles
kedro catalog list

# Ejecutar tests
kedro test

# Crear nuevo pipeline
kedro pipeline create <nombre_pipeline>

# Instalar dependencias de desarrollo
pip install -r requirements.txt
🎯 Flujo de Trabajo Recomendado
Exploración inicial: Ejecutar 02_data_understanding.ipynb

Procesamiento: Ejecutar pipeline completo con kedro run

Análisis: Usar datasets procesados para análisis estadístico

Iteración: Modificar pipelines según necesidades

📊 Datasets Generados
El pipeline produce los siguientes datasets principales:

Dataset	Descripción
games_clean	Partidos limpios
games_validated	Partidos validados
team_features_base	Features de equipos
game_level_features	Features a nivel partido
final_integrated_dataset	Dataset completo integrado

⚠️ Troubleshooting
Error	Solución
Kedro project not found	Asegúrate de estar en el directorio del proyecto:
cd nba-analysis
Missing dependencies	Reinstalar dependencias:
pip install -r requirements.txt
o instalar Kedro directamente:
pip install "kedro>=0.18.0,<0.19.0"
Dataset not found	Verificar que los archivos estén en data/01_raw/ y que conf/base/catalog.yml esté correctamente configurado