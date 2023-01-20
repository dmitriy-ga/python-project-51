install:
	poetry install

test:
	poetry run pytest page_loader

build:
	poetry build

lint:
	poetry run flake8 page_loader

test-coverage:
	poetry run pytest --cov=page_loader --cov-report xml

test-coverage-info:
	poetry run pytest --cov-report term-missing --cov=page_loader page_loader/tests/

selfcheck:
	poetry check

check: selfcheck test lint

package-install:
	python3 -m pip install --user dist/*.whl
	