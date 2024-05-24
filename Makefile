install: # Install poetry project
	poetry install

build: # Build poetry project
	poetry build

publish: # Imitate project publishing
	poetry publish --dry-run

package-install: # Install package in user environment
	python3 -m pip install --user dist/*.whl

package-reinstall: # Reinstall package in user environment
	python3 -m pip install --user dist/*.whl --force-reinstall

lint: # Run flake8 linter check
	poetry run flake8 page_analyzer

dev: # Run flask project (dev)
	poetry run flask --app page_analyzer:app run

debug: # Run flask project (debug)
	poetry run flask --app page_analyzer.app:app --debug run

PORT ?= 8000
start: # Run flask project (production)
	poetry run gunicorn -w 5 -b 0.0.0.0:$(PORT) page_analyzer:app

test: # Run pytest
	poetry run pytest

coverage: # Run coverage
	poetry run coverage run -m pytest
	poetry run coverage xml
	poetry run coverage report