#include <algorithm>
#include <apieigen/grpc/GRPCClient.hpp>
#include <chrono>
#include <fstream>
#include <iostream>
#include <random>
#include <string>
#include <vector>

std::vector<double> gen_random_vector(
    const int& size, std::default_random_engine& eng,
    std::uniform_real_distribution<double>& distr);

// Modify as needed
constexpr int MIN = 0;
constexpr int MAX = 10;

int main() {
    // Define the test file naming convention and tests to run
    const std::string file_prefix{"add_vectors_grpc["};
    const std::string file_suffix{"].txt"};
    const std::vector<int> sizes{2,   4,   8,   16,   32,  64,
                                 128, 256, 512, 1024, 2048};
    const std::vector<std::string> str_sizes{"00002", "00004", "00008", "00016",
                                             "00032", "00064", "00128", "00256",
                                             "00512", "01024", "02048"};

    // Instantiate a GRPCClient
    ansys::grpc::client::GRPCClient client{"0.0.0.0", 50000, false};

    // Instantiate our randomizer
    std::random_device rd;
    std::default_random_engine eng(rd());
    std::uniform_real_distribution<double> distr(MIN, MAX);

    // Process each of the test sizes
    std::chrono::steady_clock::time_point begin;
    std::chrono::steady_clock::time_point end;

    int idx_elem{0};
    for (const auto& elem : sizes) {
        // Define the file name and open it
        std::string elem_str_nozeros = std::to_string(elem);
        std::string file{file_prefix + str_sizes.at(idx_elem) + file_suffix};
        std::ofstream ofs;
        ofs.open(file, std::ofstream::out | std::ofstream::trunc);

        int iterations{100};
        for (int i = 0; i < iterations; i++) {
            // Get a randomized set of two vectors
            auto vec1 = gen_random_vector(elem, eng, distr);
            auto vec2 = gen_random_vector(elem, eng, distr);

            // Let us add them
            begin = std::chrono::steady_clock::now();
            client.add_vectors(vec1, vec2);
            end = std::chrono::steady_clock::now();

            // Time in seconds to output file
            ofs << std::chrono::duration_cast<std::chrono::nanoseconds>(end -
                                                                        begin)
                           .count() /
                       1000000000.0
                << std::endl;
        }

        ++idx_elem;
    }

    return 0;
}

std::vector<double> gen_random_vector(
    const int& size, std::default_random_engine& eng,
    std::uniform_real_distribution<double>& distr) {
    std::vector<double> vec{};

    for (int i = 0; i < size; i++) {
        vec.push_back(distr(eng));
    }

    return vec;
}