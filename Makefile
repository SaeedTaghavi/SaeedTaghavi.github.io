# Run from WSL/Linux in the repo folder.
#   make local                 serve at http://localhost:8000, reloads on save
#   make build                 the same strict build the deploy runs
#   make push MSG="message"    build, commit everything, push to GitHub

VENV   := .venv
PY     := $(VENV)/bin/python
STAMP  := $(VENV)/.installed
MSG    ?= Update site
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)

.PHONY: help install local build push clean

help:
	@echo "make local                 serve at http://localhost:8000"
	@echo "make build                 strict build (same as deploy)"
	@echo 'make push MSG="message"    build, commit all changes, push'
	@echo "make clean                 remove site/ and .cache/"

$(STAMP): requirements.txt
	python3 -m venv $(VENV)
	$(PY) -m pip install -q --upgrade pip
	$(PY) -m pip install -q -r requirements.txt
	@touch $(STAMP)

install: $(STAMP)

local: $(STAMP)
	$(PY) -m zensical serve

build: $(STAMP)
	$(PY) -m zensical build --strict

push: build
	git add -A
	@git diff --cached --quiet && echo "Nothing new to commit." || git commit -m "$(MSG)"
	git push origin $(BRANCH)

clean:
	rm -rf site .cache
