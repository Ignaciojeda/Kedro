#!/bin/bash
echo "🚀 Iniciando despliegue NBA ML Pipeline..."
docker build -t nba-ml .
docker run -v $(pwd)/data:/app/data nba-ml
echo "✅ Despliegue completado!"