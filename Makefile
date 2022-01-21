install:
		poetry install

build:
		poetry build

publish:
		poetry publish --dry-run

package-install:
		python3 -m pip install --user dist/*.whl

lint:
		poetry run flake8 page-loader

test:
		poetry run pytest

test-coverage:
		poetry run pytest --cov=page-loader --cov-report xml