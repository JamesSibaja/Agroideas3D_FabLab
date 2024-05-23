#!/bin/bash

# Espera a que el servidor PostgreSQL esté listo
dockerize -wait tcp://localhost:5432 -timeout 60s

# Ejecuta el comando para crear la extensión PostGIS
su - postgres -c 'psql -c "CREATE EXTENSION postgis;"'
