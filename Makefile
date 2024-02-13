.PHONY: venv test clean

VENV-BIN:=virtualenv
VENV:=venv

# Build virtual environment
venv:
	${VENV-BIN} ${VENV}/ && . ${VENV}/bin/activate && \
		pip3 install -r requirements.txt

# Run application tests
test: venv
	echo "Not implemented yet!"

# Remove virtual environment
clean:
	@rm -r venv/	
