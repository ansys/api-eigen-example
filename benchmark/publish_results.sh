#!/bin/bash

# after running the "run_tests.sh", upload the figures (to both the static folder and the docs folder)
\cp -r data/*.svg results/
\cp -r data/*.svg ../doc/source/benchmark/images/