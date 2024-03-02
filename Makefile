install: # Install project
	poetry install

build: # Build project
	poetry build

publish: # Imitate publishing
	poetry publish --dry-run

package-install: # Install package
	python3 -m pip install --user dist/*.whl

package-reinstall: # Reinstall package
	python3 -m pip install --user dist/*.whl --force-reinstall

lint: # Run flake8
	poetry run flake8

test: # Run pytest
	poetry run pytest

coverage: # Run coverage
	poetry run coverage run -m pytest
	poetry run coverage xml
	poetry run coverage report

dev:
	poetry run flask --app page_analyzer.app:app run

debug:
	poetry run flask --app page_analyzer.app:app --debug run

PORT ?= 8000
start:
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app
