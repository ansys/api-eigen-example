#!/bin/bash

# create a virtual environment and install requirements
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -q

# clear out old benchmarks (optional, should use a command line arg)
rm -rf .benchmarks

# clone api-eigen-example examples
rm -rf api-eigen-example
git clone --depth 1 https://github.com/ansys/api-eigen-example.git

# Install the eigen wrapper and requirements for api-eigen-example
pip install -r api-eigen-example/requirements/requirements_eigen_wrapper.txt
pip install api-eigen-example/src/ansys/eigen/cpp/eigen-wrapper
pip install -r api-eigen-example/requirements/requirements_build.txt

# Declare an array of string with type
declare -a Versions=(
    "main"
    )
 
# Iterate the string array using for loop
for version in ${Versions[@]}; do
    echo "Benchmarking api-eigen-example" $version
    if [ "$version" = "main" ]; then
        pip install api-eigen-example/
    else
        pip install api-eigen-example==$version -q
    fi
    pytest tests/ --benchmark-save=$version --benchmark-quiet --disable-warnings --no-header
done

mkdir hist -p
rm hist/*
pytest-benchmark compare --histogram hist/hist --group-by name --sort fullname 1> /dev/null