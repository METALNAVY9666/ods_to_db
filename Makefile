PIP=venv/bin/pip
PYTHON=venv/bin/python
VENV=venv/bin/activate
COMP=${PYTHON} -m PyInstaller
FLAGS=--onefile
HIDDEN_IMPORTS=--hidden-import pyexcel_io.writers --hidden-import pyexcel_io.readers
FILENAME=main.py
OG_EXPORTED_PATH=dist/main
BUILD_FILES=build dist main.spec
FINAL_NAME=ods_to_db

ods_to_db: ${OG_EXPORTED_PATH}
	cp ${OG_EXPORTED_PATH} ./${FINAL_NAME}

${VENV}: requirements.txt
	python -m venv venv
	. ${VENV}
	${PIP} install -r requirements.txt

${OG_EXPORTED_PATH}: ${VENV}
	. ${VENV}
	${COMP} ${FLAGS} ${HIDDEN_IMPORTS} ${FILENAME}

all: ods_to_db

clean:
	rm -rf ${BUILD_FILES}

fclean: clean
	rm -f ${FINAL_NAME}
	rm -rf venv

re: fclean all

install: all
	sudo cp ${FINAL_NAME} /usr/bin/

reinstall: fclean install

uninstall:
	sudo rm -f /usr/bin/${FINAL_NAME}

.PHONY: all clean fclean re install uninstall reinstall