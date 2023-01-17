install:
	poetry install

test:
	poetry run pytest src

build:
	poetry build

lint:
	poetry run flake8 src

test-coverage:
	poetry run pytest --cov=src --cov-report xml

test-coverage-info:
	poetry run pytest --cov-report term-missing --cov=src src/tests/

selfcheck:
	poetry check

check: selfcheck test lint

package-install:
	python3 -m pip install --user dist/*.whl
	