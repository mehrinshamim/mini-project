#!/bin/bash

echo "Starting Job Autofiller Setup..."

# 1. Check for uv
if ! command -v uv &> /dev/null; then
    echo "'uv' not found. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source $HOME/.cargo/env
fi

# 2. Install dependencies
echo "Installing backend dependencies..."
uv sync

# 3. Environment variables
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "Please update your .env file with GROQ_API_KEY and APIFY_API_TOKEN before running."
fi

# 4. Start Docker containers
echo "Starting Docker containers (db, redis)..."
docker-compose up -d db redis

# 5. Wait for DB to be ready
echo "Waiting for database to be ready..."
until docker-compose exec -T db pg_isready -U "${DB_USER:-postgres}" > /dev/null 2>&1; do
    sleep 1
done

# 6. Run migrations
echo "Running DB migrations..."
uv run alembic upgrade head

echo "Setup complete. Run 'uv run uvicorn app.main:app --reload' to start."
