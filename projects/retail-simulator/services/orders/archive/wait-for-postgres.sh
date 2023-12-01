#!/bin/bash

host="192.168.0.203"  # Name of the PostgreSQL service in your Docker Compose
port=" 55432"      # PostgreSQL port
password="password"
user="postgres"

# Wait for PostgreSQL to be ready
sleep 10;

#while ! nc -z $host $port; do
#    echo "Waiting for PostgreSQL to start..."
#    sleep 1
#done

# Wait for PostgreSQL to be ready

until PGPASSWORD="$password" psql -h "$host" -U "$user" -p "$port" -c '\q'; do
    echo "Waiting for PostgreSQL to start..."
    sleep 1
done

echo "PostgreSQL is up and running! Starting the POS app..."
exec "$@"
