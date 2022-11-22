#!/bin/sh
# wait-for-pg.sh

# A helper script which blocks the execution thread until the postgres database is up and running

PG_URL="postgresql://$NOTE_TAKER_DB_USER:$NOTE_TAKER_DB_PASSWORD@$NOTE_TAKER_DB_HOST:5432"

status=1
while [ $status -gt 0 ]
do
  psql "$PG_URL" -c "\q" > /dev/null 2>&1
  status=$?
  sleep 1
  echo "Postgres is unavailable - sleeping"
done
echo "Postgres is up - executing command"