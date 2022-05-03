#include <cstdint>
#include <random>
#include <vector>
#include <chrono>
#include <functional>
#include <iostream>
#include <algorithm>
#include <stdexcept>

template<typename T>
int64_t get_memcopy_duration(std::size_t vec_size, uint16_t repetitions, std::function<T()> item_getter) {
    // Generate source vectors
    std::vector<std::vector<T>> source_vectors;
    for(std::size_t i = 0; i < repetitions; ++i) {
        source_vectors.emplace_back(vec_size);
        std::generate(source_vectors[i].begin(), source_vectors[i].end(), item_getter);
    }

    // Create empty target vectors
    std::vector<std::vector<int32_t>> target_vectors;
    for(std::size_t i = 0; i < repetitions; ++i) {
        target_vectors.emplace_back(vec_size);
    }

    // Copy from source to target
    auto start = std::chrono::high_resolution_clock::now();
    for(std::size_t i = 0; i < repetitions; ++i) {
        std::copy(source_vectors[i].cbegin(), source_vectors[i].cend(), target_vectors[i].begin());
    }
    auto stop = std::chrono::high_resolution_clock::now();

    int64_t duration = std::chrono::duration_cast<std::chrono::nanoseconds>(stop - start).count();

    // Check for correctness, also to trick the compiler into keeping the
    // above operations.
    for(std::size_t i = 0; i < repetitions; ++i) {
        for(std::size_t j = 0; j < vec_size; ++j) {
            if(source_vectors[i][j] != target_vectors[i][j]) {
                throw std::runtime_error("Vectors do not match.");
            }
        }
    }
    return duration;
}

int main() {
    using measured_type = int32_t;

    std::random_device rnd_device;
    // We don't particularly care for the quality of random numbers.
    std::minstd_rand random_engine {rnd_device()};
    std::uniform_int_distribution<int32_t> dist;

    uint16_t repetitions = 15;
    int64_t duration = 0;
    std::cout << "size_bytes,repetitions,duration_nanoseconds" << std::endl;
    for(std::size_t size_pow=10; size_pow < 25; ++size_pow) {
        std::size_t size = std::size_t(1) << size_pow;
        duration = get_memcopy_duration<measured_type>(size, repetitions, [&](){return dist(random_engine);});
        std::cout << size * sizeof(measured_type) << "," << repetitions << "," << duration << std::endl;
        if(duration > 1e9) {
            repetitions /= 2;
            if(repetitions == 0) {
                break;
            }
        }
    }
}
