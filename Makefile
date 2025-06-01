# Variables
APP_NAME = ./order_service/order_api/src/order_api/main
TESTS_DIRECTORY=./order_service/order_api/src/order_api/tests/

# Default target
.PHONY: run
run:
	FLASK_APP=$(APP_NAME) flask run --debug

# Run unit tests
.PHONY: test
test:
	python -m unittest discover -s $(TESTS_DIRECTORY)

# Run pytest if available
.PHONY: pytest
pytest:
	pytest $(TESTS_DIRECTORY)

# Format code using black
.PHONY: format
format:
	black .

# Lint using flake8
.PHONY: lint
lint:
	flake8 .

# Clean __pycache__ and .pyc files
.PHONY: clean
clean:
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type f -name '*.pyc' -delete

# start infra with kafka
.PHONY: infra-up
infra-up:
	sudo docker compose up -d


.PHONY: infra-down
infra-down:
	sudo docker compose down