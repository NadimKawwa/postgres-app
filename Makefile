.PHONY: postgres postgres-up postgres-down postgres-shell postgrest postgrest-down seed test up down network

NETWORK=pgnet

postgres-data:
	mkdir -p postgres-data 

network:
	docker network create $(NETWORK) 2>/dev/null || true

postgres: postgres-data network
	docker run -d --rm \
	--name pgdb \
	--network $(NETWORK) \
	--env-file .env \
	-p 54320:5432 \
	-v $$(pwd)/postgres-data:/var/lib/postgresql/data \
	pgvector/pgvector:pg17 

postgres-down:
	docker stop pgdb 2>/dev/null || true 

postgres-shell:
	docker exec -it pgdb psql -U $$(grep POSTGRES_USER .env | cut -d= -f2) -d postgres

# PostgREST
postgrest: network
	@# Generate connection string using Python to handle URL encoding
	@export DB_URI=$$(uv run python -c "import os, urllib.parse; from dotenv import load_dotenv; load_dotenv(); print(f'postgres://{os.getenv('POSTGRES_USER')}:{urllib.parse.quote_plus(os.getenv('POSTGRES_PASSWORD'))}@pgdb:5432/postgres')") && \
	docker run -d --rm --name postgrest \
	--network $(NETWORK) \
	-p 3005:3000 \
	-e PGRST_DB_URI="$$DB_URI" \
	-e PGRST_DB_SCHEMAS=public \
	-e PGRST_DB_ANON_ROLE=$$(grep POSTGRES_USER .env | cut -d= -f2) \
	postgrest/postgrest


postgrest-down:
	docker stop postgrest 2>/dev/null || true

# Operations
seed:
	uv run python scripts/seed_db.py

test:
	uv run python scripts/test_api.py

search-demo:
	uv run python features/search.py

# Full Workflow
up: postgres
	@echo "Waiting for Postgres to be ready..."
	@sleep 5
	uv run python sql/init_db.py
	@echo "Starting PostgREST..."
	$(MAKE) postgrest
	@echo "App is running! API at http://localhost:3005"

down: postgrest-down postgres-down
	docker network rm $(NETWORK) 2>/dev/null || true