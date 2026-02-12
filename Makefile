DC = docker-compose
EXEC = docker exec -it
APP_CONTAINER = backend

# Хак для передачи имен сервисов напрямую: make up backend worker
# MAKECMDGOALS - это все слова, что ты ввел после make
# filter-out удаляет саму команду (например, 'up') из списка аргументов
ARGS = $(filter-out $@,$(MAKECMDGOALS))

# Служебная цель, чтобы make не ругался на имена сервисов как на неизвестные команды
%:
	@:

.PHONY: help setup build up stop down restart logs migrate lint

# По умолчанию выводим помощь
help:
	@echo "Использование: make [команда] [сервисы...]"
	@echo ""
	@echo "Команды:"
	@echo "  setup     Собрать проект и пролить миграции"
	@echo "  build     Собрать образы"
	@echo "  up        Запустить контейнеры (в фоне)"
	@echo "  up-build  Собрать образы и сразу запустить контейнеры"
	@echo "  stop      Остановить контейнеры"
	@echo "  down      Удалить контейнеры и сети"
	@echo "  restart   Перезапустить сервисы"
	@echo "  logs      Посмотреть логи"
	@echo "  migrate   Запустить миграции БД"
	@echo "  lint      Проверить и отформатировать код (Ruff)"
	@echo "  clean     Удалить неиспользуемые образы и тома"

# Полная настройка с нуля
setup: build migrate

build:
	$(DC) build $(ARGS)

up:
	$(DC) up -d $(ARGS)

up-build:
	$(DC) up -d --build $(ARGS)

stop:
	$(DC) stop $(ARGS)

down:
	$(DC) down $(ARGS)

down-v:
	$(DC) down -v $(ARGS)

restart:
	$(DC) stop $(ARGS)
	$(DC) up -d $(ARGS)

logs:
	$(DC) logs -f $(ARGS)

migrate:
	$(DC) run --rm migrations

lint:
	ruff check . --fix
	ruff format .

clean:
	docker system prune -a --volumes -f
