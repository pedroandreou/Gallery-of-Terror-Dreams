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

.PHONY: update-and-pin-requirements-txt
update-and-pin-requirements-txt: VENV := /tmp/venv/
update-and-pin-requirements-txt: ## Update and Pin ./src/front-end/unpinned_requirements & ./src/back-end/unpinned_requirements
	@if [ -d ${VENV} ]; then rm -rf ${VENV}; fi
	@mkdir ${VENV}
	${PYTHON} -m venv ${VENV}
	${VENV}/bin/pip install --upgrade pip==22.2.2
	(cat src/back-end/unpinned_requirements.txt; cat src/front-end/unpinned_requirements.txt | sort | uniq) | ${VENV}/bin/pip install -r /dev/stdin
	echo "# Created automatically by make update-and-pin-requirements-txt. Do not update manually!" > requirements.txt
	${VENV}/bin/pip freeze | grep -v pkg_resources >> requirements.txt
	for dir in src/back-end src/front-end; do \
		rm -f $$dir/pinned_requirements.txt && \
		cat $$dir/unpinned_requirements.txt | \
		xargs pip show | \
		awk '/^Name:/ {name=$$2} /^Version:/ {print name "==" $$2}' | \
		sort | uniq > $$dir/pinned_requirements.txt; \
	done

.PHONY: clean
clean: ## Clean python cache
	find . -type d -name "__pycache__" -exec rm -rf {} \;
