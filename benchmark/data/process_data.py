import csv
import glob
import statistics

import matplotlib.pyplot as plt
import pandas as pd

MICRO = 1e6

# First, read the Python results
python_tests = pd.read_csv("python_bm_results.csv", sep=",", header=0, index_col=0)
python_tests.filter(items=["name", "mean"])

# Now, find all C++ result files
cpp_tests_txt = glob.glob("*.txt")
cpp_tests_dict = {}
for file in cpp_tests_txt:
    with open(file) as inf:
        reader = csv.reader(inf, delimiter=" ", quoting=csv.QUOTE_NONNUMERIC)
        avg = statistics.mean(list(zip(*reader))[0])
        cpp_tests_dict[file] = (file, avg)

cpp_tests = pd.DataFrame(cpp_tests_dict)
cpp_tests = cpp_tests.transpose()
cpp_tests.set_axis(labels=["name", "mean"], axis=1)

print("Data parsed!")

# Plotting vector addition
for test_type in [
    "add_vectors",
    "multiply_vectors",
    "add_matrices",
    "multiply_matrices",
]:

    print("Plotting %s test..." % test_type)

    rest_python = grpc_python = rest_cpp = grpc_cpp = None
    rest_python = python_tests.filter(axis=0, like="test_%s_rest_python" % test_type)[
        "mean"
    ].to_numpy()
    grpc_python = python_tests.filter(axis=0, like="test_%s_grpc_python" % test_type)[
        "mean"
    ].to_numpy()
    rest_cpp = (
        cpp_tests.filter(axis=0, like="%s_rest" % test_type)
        .sort_values(by=[0], ascending=True)[1]
        .to_numpy()
    )
    grpc_cpp = (
        cpp_tests.filter(axis=0, like="%s_grpc" % test_type)
        .sort_values(by=[0], ascending=True)[1]
        .to_numpy()
    )
    x_axis = ["2", "4", "8", "16", "32", "64", "128"]

    figure = plt.figure()
    plt.plot(
        x_axis,
        rest_python * MICRO,
        color="green",
        marker="o",
        linestyle="dashed",
        linewidth=2,
        markersize=12,
    )
    plt.plot(
        x_axis,
        grpc_python * MICRO,
        color="red",
        marker="o",
        linestyle="dashed",
        linewidth=2,
        markersize=12,
    )
    plt.plot(
        x_axis,
        rest_cpp * MICRO,
        color="blue",
        marker="o",
        linestyle="dashed",
        linewidth=2,
        markersize=12,
    )
    plt.plot(
        x_axis,
        grpc_cpp * MICRO,
        color="black",
        marker="o",
        linestyle="dashed",
        linewidth=2,
        markersize=12,
    )
    plt.xlabel("Number of elements [-]")
    plt.ylabel("Duration [us]")
    plt.title("Avg. Speed in microseconds [us] of %s" % test_type)
    plt.grid(alpha=0.5, linestyle="dashed")
    plt.legend(
        ["REST - Python", "gRPC - Python", "REST - C++", "gRPC - C++"],
        loc="upper center",
        bbox_to_anchor=(0.5, -0.15),
        fancybox=True,
        shadow=True,
        ncol=4,
    )
    plt.tight_layout()
    figure.savefig("%s.svg" % test_type, format="svg")

    print("Plot for %s test saved!" % test_type)
