#!/bin/bash
# setup.sh

# # 1. Create PostgreSQL database
# psql -U postgres -c "CREATE DATABASE myapp;"
# psql -U postgres -d myapp -c "CREATE EXTENSION IF NOT EXISTS vector;"

# # 2. Setup Python environment
# python3 -m venv .venv
# source .venv/bin/activate

# # 3. Install dependencies
# pip install -r requirements.txt

uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# # 4. Run migrations (create tables)
# psql -U postgres -d myapp -f schema.sql

# # 5. Start server
# uvicorn app:app --reload --port 8000