# Run from WSL/Linux in the repo folder.
#   make local                 serve at http://localhost:8000, reloads on save
#                              (stops any server already running first)
#   make stop                  stop a running preview server
#   make build                 the same strict build the deploy runs
#   make push MSG="message"    build, commit everything, push to GitHub
#
# Note: `make build` writes to site/, the same folder `make local` serves.
# Run `make local` again after a build to get the live preview back.

VENV   := .venv
PY     := $(VENV)/bin/python
STAMP  := $(VENV)/.installed
MSG    ?= Update site
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
PORT   := 8000
# The brackets stop pgrep/pkill from matching the shell that runs the command.
SERVE  := [z]ensical serve

.PHONY: help install local stop status build push clean

help:
	@echo "make local                 serve at http://localhost:$(PORT) (stops an old server first)"
	@echo "make stop                  stop a running preview server"
	@echo "make status                show whether a preview server is running"
	@echo "make build                 strict build (same as deploy)"
	@echo 'make push MSG="message"    build, commit all changes, push'
	@echo "make clean                 remove site/ and .cache/"

$(STAMP): requirements.txt
	python3 -m venv $(VENV)
	$(PY) -m pip install -q --upgrade pip
	$(PY) -m pip install -q -r requirements.txt
	@touch $(STAMP)

install: $(STAMP)

local: $(STAMP) stop
	$(PY) -m zensical serve --dev-addr localhost:$(PORT)

stop:
	@if pkill -f "$(SERVE)"; then \
		echo "Stopped the running preview server."; \
		while pgrep -f "$(SERVE)" >/dev/null; do sleep 0.2; done; \
	else \
		echo "No preview server running."; \
	fi

status:
	@pgrep -af "$(SERVE)" || echo "No preview server running."

build: $(STAMP)
	$(PY) -m zensical build --strict

push: build
	git add -A
	@git diff --cached --quiet && echo "Nothing new to commit." || git commit -m "$(MSG)"
	git push origin $(BRANCH)

clean:
	rm -rf site .cache
