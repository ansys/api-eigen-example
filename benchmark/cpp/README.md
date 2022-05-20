# API Eigen Example Benchmarks using C++

Benchmarks for [API Eigen Example](https://github.com/ansys/api-eigen-example) using C++ (for both REST and gRPC).

In order to have the same look and feel as the Python benchamrk tests, a binding to the C++ libraries was performed. In fact, for running these tests, it is necessary to actually deploy the servers (this will be done automatically using the ``run_tests.sh``bash script). However, it is necessary to have installed ``docker`` in your OS.

Run with
```
./run_tests.sh
```

Output will be saved to `hist/`. In case you want to store the new benchmark test results, please run:
```
./publish_results.sh
```

And commit to the repository.

## Results

Please, refer to the following [file](https://github.com/ansys/api-eigen-example/edit/feat/bm-results/benchmark/cpp/results/README.md) for going through the latest benchmark results published.
