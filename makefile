activate:
	if [ -d "venv" ]; then \
        echo "Python 🐍 environment was activated"; \
    else \
        echo "The folder environment doesn't exist"; \
		python -m venv venv; \
        echo "The environment folder was created and the python 🐍 environment was activated"; \
    fi
	. ./venv/bin/activate

install:
	pip3 install -r requirements.txt

run:
	@if [ -z "$(strip $(PORT))" ]; then \
		flask --app ./src run; \
	else \
		flask --app ./src run -p $(PORT); \
	fi

run-docker:
ifeq ($(strip $(PORT)),)
	flask --app ./src run -h 0.0.0.0
else
	flask --app ./src run -p $(PORT) -h 0.0.0.0
endif

run-tests:
	FLASK_ENV=test coverage run -m pytest

run-tests-coverage:
	 make run-tests
	 coverage report

docker-up:
	docker compose up --build

docker-down:
	docker compose down

docker-local-up:
	docker compose -f=docker-compose.local.yaml up --build

docker-local-down:
	docker compose -f=docker-compose.local.yaml down