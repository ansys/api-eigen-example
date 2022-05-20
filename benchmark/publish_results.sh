#!/bin/bash

# after running the "run_tests.sh", upload the figures (to both the static folder and the docs folder)
\cp -r hist/* results/
\cp -r hist/* ../doc/source/benchmark/images/