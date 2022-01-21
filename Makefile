install:
		poetry install

publish:
		poetry publish --dry-run

package-install:
		python3 -m pip install --user dist/*.whl

lint:
		poetry run flake8 gendiff

test:
		poetry run pytest

test-coverage:
		poetry run pytest --cov=page-loader --cov-report xml