.PHONY: postgres postgres-up postgres-down postgres-shell

postgres-data:
	mkdir -p postgres-data 

postgres: postgres-data
	docker run -d --rm \
	--name pgdb \
	--env-file .env \
	-p 54320:5432 \
	-v $$(pwd)/postgres-data:/var/lib/postgresql/data \
	pgvector/pgvector:pg17 

postgres-down:
	docker stop postgres-app 2>/dev/null || true 
	docker rm pgdb 2>/dev/null || true 

postgres-shell:
	docker exec -it pgdb psql -U $$(grep POSTGRES_USER .env | cut -d= -f2) -d postgres 