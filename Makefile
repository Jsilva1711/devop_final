PYTHON = python3

build-up:
	$(PYTHON) ctf-create.py && docker-compose build --no-cache && docker-compose up -d

build:
	$(PYTHON) ctf-create.py && docker-compose build

up:
	docker-compose up -d

down:
	docker-compose down

shell:
	docker exec -it ctf-admin bash

clean:
	rm -rf env __pycache__
