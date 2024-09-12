##
# REX - exchange rates
#

# dependencies
install:
	pip install -r requirements.lock

install-dev:
	pip install -r requirements_dev.txt

install-pre-commit:
	@pre-commit install && pre-commit install --hook-type commit-msg

# running
run: stop
	sh containers.sh

stop:
	podman stop --all

# checkers
check:
	pre-commit run --all-files

format:
	ruff format

test:
	pytest
# end
