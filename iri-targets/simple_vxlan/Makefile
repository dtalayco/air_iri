# Make file for simple VXLAN target

TOP_DIR=../..
OFTEST_PATH=${TOP_DIR}/submodules/oftest
OFTEST_PYTHON=${OFTEST_PATH}/src/python

SWITCH_NAME=vxlan

THRIFT_INPUT_DIR=thrift
THRIFT_FILE_NAME=${THRIFT_INPUT_DIR}/table_intf.thrift
THRIFT_OUTPUT_DIR=runtime_lib
THRIFT_TEMPLATE_DIR=${TOP_DIR}/templates

THRIFT_PY_PATH=${THRIFT_OUTPUT_DIR}/${SWITCH_NAME}_rpc
PYPATH=PYTHONPATH=${TOP_DIR}:${OFTEST_PYTHON}:${THRIFT_PY_PATH}

INPUT_FILES=${wildcard *.yml}

CREATE_THRIFT_EXE=${TOP_DIR}/create_thrift_input.py
CREATE_THRIFT_ARGS=-o ${THRIFT_INPUT_DIR} -n ${SWITCH_NAME} -t ${THRIFT_TEMPLATE_DIR}

#include ../common.mk

start: submodule runtime
	sudo ${PYPATH} ${TOP_DIR}/start.py -v ${INPUT_FILES}

submodule:
	git submodule update --init

${THRIFT_FILE_NAME}: ${INPUT_FILES}
	@mkdir -p ${THRIFT_INPUT_DIR}
	${PYPATH} ${CREATE_THRIFT_EXE} ${INPUT_FILES} ${CREATE_THRIFT_ARGS}

runtime: ${THRIFT_FILE_NAME}
	mkdir -p ${THRIFT_OUTPUT_DIR}
	thrift -r --gen py --out ${THRIFT_OUTPUT_DIR} ${THRIFT_FILE_NAME}

.PHONY: submodule clean test start help
