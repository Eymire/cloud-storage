#!/usr/bin/env bash

echo "Start migrations..."
uv run alembic upgrade head
echo "Migrations complete!"

if [ -f ./certificates/jwt-private.pem ] && [ -f ./certificates/jwt-public.pem ]; then
	echo "JWT keys already exist. Skipping generation."
else
	echo "Generating JWT keys..."
	openssl genrsa -out ./certificates/jwt-private.pem 2048
	openssl rsa -in ./certificates/jwt-private.pem -outform PEM -pubout -out ./certificates/jwt-public.pem
	echo "JWT keys generated!"
fi

exec "$@"
