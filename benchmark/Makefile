# This Makefile ties together the steps required to install C++ and
# Python dependencies. It only works on Linux, but can serve as
# self-documenting instructions for building on Windows.
# As such, they are ordered roughly in chronological order.

# Commands with a preceding '@' are for the purposes of make only,
# there is no need to reproduce then on Windows.

PROTOC=build/protoc
PROTOS_DIR=src/protos
GRPC_CPP_PLUGIN_PATH=build/grpc_cpp_plugin
VENV_ACTIVATE=venv/bin/activate

SHELL := /bin/bash

UNCONSTRAINED_RESULT_FILES= results/sync.csv results/threaded_client.csv
CONSTRAINED_RESULT_FILES= results/rate_100mbit.csv results/delay_1ms.csv results/compressionlevel_3_rate_100mbit.csv

all: compile_project $(UNCONSTRAINED_RESULT_FILES) $(CONSTRAINED_RESULT_FILES)

venv/bin/activate:
	@echo "### Creating Python virtual environment ###"
	python3 -m venv venv

venv/.done: requirements.txt venv/bin/activate
	@echo "### Installing Python dependencies ###"
	. $(VENV_ACTIVATE) && \
	pip install -U pip && \
	pip install -r requirements.txt && \
	conan profile new --detect --force grpc_cpp_benchmark && \
	conan profile update settings.compiler.libcxx=libstdc++11 grpc_cpp_benchmark && \
	conan remote add -f conancenter https://center.conan.io
	@touch $@

RENDERED_TEMPLATE_FILES= src/protos/send_array.proto src/common/types_lookup.hpp src/client/sync_client.cpp src/server/sync_server.cpp src/client/sync_client_fixed_chunksize.cpp

$(RENDERED_TEMPLATE_FILES): % : render_templates.py venv/.done %.in
	@echo "### Rendering input file from template ###"
	. $(VENV_ACTIVATE) && python $< $@.in $@

build/.deps_done: conanfile.txt venv/.done
	@echo "### Installing C++ dependencies ###"
	mkdir -p build
	. $(VENV_ACTIVATE) && conan install -if build --build=* --profile=grpc_cpp_benchmark .
	@touch $@

generated_src/.generate_done: src/protos/send_array.proto build/.deps_done
	@echo "### Compiling .proto file to C++ source ###"
	$(PROTOC) --proto_path=$(PROTOS_DIR) --cpp_out=generated_src --grpc_out=generated_src --plugin=protoc-gen-grpc=$(GRPC_CPP_PLUGIN_PATH) send_array.proto
	@touch $@

BIN_OUTPUT_FILES= build/bin/measure_memcpy build/bin/sync_client build/bin/sync_client_fixed_chunksize build/bin/sync_server

$(BIN_OUTPUT_FILES): compile_project;

compile_project: build/.deps_done generated_src/.generate_done $(RENDERED_TEMPLATE_FILES) CMakeLists.txt **/CMakeLists.txt
	@echo "### Setting up CMake ###"
	cd build && cmake ..
	@echo "### Compiling the C++ source ###"
	$(MAKE) -C build

$(UNCONSTRAINED_RESULT_FILES): run_unconstrained_measurements;
run_unconstrained_measurements: runner/run_measurements.py build/bin/sync_client build/bin/sync_server
	@echo "### Running unconstrained measurements ###"
	. $(VENV_ACTIVATE) && python $<


$(CONSTRAINED_RESULT_FILES): runner/run_constrained.py build/bin/sync_client_fixed_chunksize build/bin/sync_server
	@echo "### Running constrained measurements ###"
	. $(VENV_ACTIVATE) && python $< $@

results/memcpy.csv: build/bin/measure_memcpy
	build/bin/measure_memcpy > $@

clean:
	rm -rf venv
	rm -rf build
	rm -rf generated_src/*.cc
	rm -rf generated_src/*.h
	rm -rf **/.*done
	rm -f src/protos/*.proto
	rm -f src/types_lookup.hpp
	rm -f results/*.csv

.PHONY: clean compile_project all run_constrained_measurements
