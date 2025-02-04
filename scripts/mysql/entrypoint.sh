#!/bin/bash
set -e

# Check if APP_ENV is set to "dev"
if [ "$APP_ENV" = "dev" ]; then
    echo "Running extra SQL script for development..."
    mysql -u root -p"${MYSQL_ROOT_PASSWORD}" "${MYSQL_DATABASE}" < /docker-entrypoint-initdb.d/dev_extra.sql
else
    echo "Skipping extra SQL script. APP_ENV is not 'dev'."
fi

# Keep the container running
exec "$@"
