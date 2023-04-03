SHELL=./make-venv
SHELL := /bin/sh

.DEFAULT_GOAL := help

VENV := .env
PYTHON := python3.8

.PHONY: virtualenv
virtualenv: ## Create virtualenv
	@if [ -d ${VENV} ]; then rm -rf ${VENV}; fi
	@mkdir ${VENV}
	${PYTHON} -m venv ${VENV}
	${VENV}/bin/pip install --upgrade pip==22.2.2
	${VENV}/bin/pip install -r requirements.txt

.PHONY: update-requirements-txt
update-requirements-txt: VENV := /tmp/venv/
update-requirements-txt: ## Update requirements.txt
	@if [ -d ${VENV} ]; then rm -rf ${VENV}; fi
	@mkdir ${VENV}
	${PYTHON} -m venv ${VENV}
	${VENV}/bin/pip install --upgrade pip==22.2.2
	(cat src/back-end/pinned_requirements.txt; cat src/front-end/pinned_requirements.txt | sort | uniq) | ${VENV}/bin/pip install -r /dev/stdin
	echo "# Created automatically by make update-requirements-txt. Do not update manually!" > requirements.txt
	${VENV}/bin/pip freeze | grep -v pkg_resources >> requirements.txt

.PHONY: clean
clean: ## Clean python cache
	find . -type d -name "__pycache__" -exec rm -rf {} \;
