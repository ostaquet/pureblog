.PHONY: up down shell opencode restart clean purge logs status

up:
	docker compose up -d --build
	@echo "Containers started. Use 'make shell' or 'make opencode' to access dev environment"

down:
	docker compose down

shell:
	docker compose exec dev bash

opencode:
	docker compose exec dev opencode_start

restart: down up

clean: down
	docker compose down --rmi all --volumes

purge: clean
	docker system prune --all --force

logs:
	docker compose logs -f

ps:
	docker compose ps
