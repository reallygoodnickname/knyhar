.PHONY: venv test clean

VENV-BIN:=virtualenv
VENV:=venv

# Build virtual environment
venv:
	@${VENV-BIN} -q ${VENV}/ && . ${VENV}/bin/activate && \
		pip3 install -q -r requirements.txt

# Run application tests
tests: venv
	@. ${VENV}/bin/activate && \
	coverage run -m unittest discover -s tests && \
	coverage report -m --skip-covered --omit="tests/*,knyhar/models/*" && \
	coverage html

# Remove virtual environment
clean:
	@rm -r venv/	
