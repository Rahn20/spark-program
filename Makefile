#!/usr/bin/env make
# Make file for Scooter program
# -----------------------------------------------------------------------------
#

check-version:
	uname -a
	@which make
	make --version
	@which python3
	python3 --version
	@which pip3
	pip3 --version



# Remove all generated files.
clean:
	rm -rf __pycache__
	rm -rf src/__pycache__
	rm -rf tests/__pycache__
	rm .coverage
	rm -rf htmlcov

# Remove all installed files.
clean-all:
	rm -rf .venv


# Install Python utilities locally.
install:
	[ ! -f requirements.txt ] || python3 -m pip install --requirement requirements.txt

# Upgrade Python utilities locally.
upgrade:
	[ ! -f requirements.txt ] || python3 -m pip install --upgrade --requirement requirements.txt


# Create Python virtual environment .venv.
venv:
	python3 -m venv .venv


# Run tests.
test:
	python3 test.py

# Run pylint.
lint:
	pylint src/ tests/ main.py


# Review code coverage.
# Run the coverage module to generate the coverage data and turn the coverage data into a report.
coverage:
	coverage run --source=src -m unittest
	coverage report -m

# Run the coverage module to generate the coverage data and generate the coverage report in HTML format.
coverage-html:
	coverage run --source=src -m test
	python3 -m coverage html

test-all: lint coverage
