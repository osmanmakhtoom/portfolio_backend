#!/bin/bash
set -e

DB_NAME="${DB_NAME:-portfolio}"
DB_USER="${DB_USER:-portfolio_user}"
DB_PASSWORD="${DB_PASSWORD:-supersecretpassword}"

echo "Initializing Postgres DB: $DB_NAME, User: $DB_USER"

# Connect to Postgres as superuser
psql -v ON_ERROR_STOP=1 --username "$DB_USER" --dbname "postgres" <<-EOSQL

-- Create role if it doesn't exist
DO
\$do\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_catalog.pg_roles WHERE rolname = '${DB_USER}') THEN
      CREATE ROLE ${DB_USER} LOGIN PASSWORD '${DB_PASSWORD}';
   END IF;
END
\$do\$;

-- Create database if it doesn't exist
DO
\$do\$
BEGIN
   IF NOT EXISTS (SELECT FROM pg_database WHERE datname = '${DB_NAME}') THEN
      CREATE DATABASE ${DB_NAME} OWNER ${DB_USER};
   END IF;
END
\$do\$;

-- Grant privileges (redundant if owner is already DB owner, but safe)
GRANT ALL PRIVILEGES ON DATABASE ${DB_NAME} TO ${DB_USER};

-- Optional: create schema if not exists
CREATE SCHEMA IF NOT EXISTS portfolio_schema AUTHORIZATION ${DB_USER};

EOSQL

echo "Postgres initialization completed."
