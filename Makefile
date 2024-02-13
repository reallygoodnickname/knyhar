.PHONY: venv test clean

VENV-BIN:=virtualenv
VENV:=venv

# Build virtual environment
venv:
	@${VENV-BIN} -q ${VENV}/ && . ${VENV}/bin/activate && \
		pip3 install -q -r requirements.txt

# Run application tests
tests: venv
	@python -m unittest discover -s tests

# Remove virtual environment
clean:
	@rm -r venv/	
