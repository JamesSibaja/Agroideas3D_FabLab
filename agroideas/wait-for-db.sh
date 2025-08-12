#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

until pg_isready -h "$host" -p 5432; do
  echo "Esperando base de datos en $host..."
  sleep 2
done

echo "Base de datos disponible, ejecutando comando: $cmd"
exec $cmd
