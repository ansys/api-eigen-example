# This Makefile ties together the steps required to install C++ and
# Python dependencies. It only works on Linux, but can serve as
# self-documenting instructions for building on Windows.
# As such, they are ordered roughly in chronological order.

# Commands with a preceding '@' are for the purposes of make only,
# there is no need to reproduce then on Windows.

PROTOC=build/protoc
PROTOS_DIR=../../../protos
GRPC_CPP_PLUGIN_PATH=build/grpc_cpp_plugin
VENV_ACTIVATE=.venv/bin/activate

SHELL := /bin/bash

all: compile_project

.venv/bin/activate:
	@echo "### Creating Python virtual environment ###"
	python3 -m venv .venv

.venv/.done: requirements.txt .venv/bin/activate
	@echo "### Installing Python dependencies ###"
	. $(VENV_ACTIVATE) && \
	pip install -U pip && \
	pip install -r requirements.txt && \
	conan profile new --detect --force grpc_cpp_server && \
	conan profile update settings.compiler.libcxx=libstdc++11 grpc_cpp_server && \
	conan remote add -f conancenter https://center.conan.io
	@touch $@

build/.deps_done: conanfile.txt .venv/.done
	@echo "### Installing C++ dependencies ###"
	mkdir -p build
	. $(VENV_ACTIVATE) && conan install -if build --build=* --profile=grpc_cpp_server .
	@touch $@

src/generated/.generate_done: $(PROTOS_DIR)/grpcdemo.proto build/.deps_done
	@echo "### Compiling .proto file to C++ source ###"
	$(PROTOC) \
      --proto_path=$(PROTOS_DIR) \
      --cpp_out=src/generated \
      --grpc_out=src/generated \
      --plugin=protoc-gen-grpc=$(GRPC_CPP_PLUGIN_PATH) \
      grpcdemo.proto
	@touch $@

compile_project: build/.deps_done src/generated/.generate_done CMakeLists.txt
	@echo "### Setting up CMake ###"
	cd build && cmake ..
	@echo "### Compiling the C++ source ###"
	$(MAKE) -C build

install: build/.deps_done src/generated/.generate_done CMakeLists.txt
	@echo "### Setting up CMake ###"
	cd build && cmake ..
	@echo "### Compiling the C++ source ###"
	$(MAKE) -C build install

clean:
	rm -rf .venv
	rm -rf build/*
	rm -rf src/generated/*
	rm -rf **/.*done

.PHONY: clean compile_project all
