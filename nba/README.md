📋 Descripción del Proyecto
Este proyecto analiza datos de la NBA para identificar patrones de rendimiento de equipos, especialmente el desempeño como local vs. visitante. Utiliza el framework Kedro para crear pipelines reproducibles de procesamiento de datos.

🎯 Objetivos Principales
Identificar qué equipos son mejores jugando en casa

Analizar qué equipos son peores como visitantes

Estudiar patrones ofensivos y defensivos

Crear pipelines modulares y reproducibles

📊 Datasets Utilizados
El proyecto utiliza 3 datasets principales de Kaggle NBA Games:

games.csv - Resultados y estadísticas de partidos

games_details.csv - Estadísticas por jugador por partido

teams.csv - Información de los equipos

🚀 Instalación y Configuración
Prerrequisitos
Python 3.8+

pip

virtualenv (recomendado)

1. Clonar y Configurar el Proyecto
bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual (Linux/Mac)
source venv/bin/activate

# Activar entorno virtual (Windows)
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
2. Configurar los Datos
bash
# Crear estructura de carpetas de datos
mkdir -p data/01_raw

# Descargar datasets de Kaggle y colocarlos en:
# data/01_raw/games.csv
# data/01_raw/games_details.csv  
# data/01_raw/teams.csv

3. Configurar Kedro
bash
# Inicializar proyecto (si es necesario)
kedro info

🏃‍♂️ Ejecución del Proyecto
Ejecutar el Pipeline Completo
bash
# Ejecutar todo el pipeline
kedro run
Ejecutar Pipelines Específicos
bash
# Solo data engineering
kedro run --pipeline=data_engineering

# Solo un nodo específico
kedro run --node=clean_games_data_node
Visualizar el Pipeline
bash
# Iniciar interfaz visual
kedro viz

# Abrir en navegador: http://127.0.0.1:4141
Trabajar con Notebooks
bash
# Abrir Jupyter con contexto de Kedro
kedro jupyter notebook

# O abrir notebook específico
kedro jupyter notebook --notebook-path notebooks/03_data_preparation.ipynb
📝 Notebooks Disponibles
1. 01_business_understanding.ipynb
Definición de objetivos del proyecto

Preguntas de negocio

Plan del proyecto

2. 02_data_understanding.ipynb
Análisis exploratorio de datos (EDA)

Validación de calidad de datos

Visualizaciones iniciales

3. 03_data_preparation.ipynb
Limpieza y transformación de datos

Feature engineering

Preparación para modelado

🔧 Comandos Útiles
bash
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

Procesamiento: Ejecutar pipeline completo kedro run

Análisis: Usar datasets procesados para análisis

Iteración: Modificar pipelines según necesidades

📊 Datasets Generados
El pipeline produce estos datasets principales:

games_clean - Partidos limpios

games_validated - Partidos validados

team_features_base - Features de equipos

game_level_features - Features a nivel partido

final_integrated_dataset - Dataset completo integrado

⚠️ Problemas comunes
Error: "Kedro project not found"
bash
# Asegurarse de estar en el directorio del proyecto
cd nba-analysis

# Verificar que existe pyproject.toml
ls -la pyproject.toml
Error: Missing dependencies
bash
# Reinstalar dependencias
pip install -r requirements.txt

# O instalar Kedro específicamente
pip install "kedro>=0.18.0,<0.19.0"
Error: Dataset not found
bash
# Verificar que los archivos están en data/01_raw/
ls -la data/01_raw/

# Verificar el catalog.yml
cat conf/base/catalog.yml
