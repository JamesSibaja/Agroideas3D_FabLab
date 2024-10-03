#!/bin/bash

# Espera a que el servidor PostgreSQL esté listo
until psql -h localhost -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c '\q'; do
  echo "Esperando a que PostgreSQL esté listo..."
  sleep 2
done

# Crea la extensión PostGIS si no existe
echo "Habilitando la extensión PostGIS en la base de datos..."
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE EXTENSION IF NOT EXISTS postgis;"
