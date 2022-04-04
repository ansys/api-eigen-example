#include <cstdio>
#include <cstdint>
#include <vector>
#include <chrono>
#include <algorithm>
#include <functional>

#include <grpcpp/grpcpp.h>

#include <types_lookup.hpp>
#include "send_array.grpc.pb.h"
#include "clientlib.hpp"
#include "omp.h"

namespace send_array {

template<typename GrpcType>
int64_t measure_runtime(
    ArrayServiceClient<GrpcType>& client,
    std::function<void(std::vector<typename TypesLookup<GrpcType>::data_type> &, const array_id_type)> array_getter,
    std::size_t vec_size,
    std::size_t num_repetitions,
    std::size_t num_preheat,
    std::function<typename TypesLookup<GrpcType>::data_type()> item_generator
) {
    using vector_type = typename TypesLookup<GrpcType>::vector_type;

    auto num_vectors = num_repetitions + num_preheat;

    // Fill source vectors and send them to the server
    std::vector<vector_type> source_vectors(num_repetitions + num_preheat);
    client.DeleteArrays();
    for(auto &vec: source_vectors) {
        vec.resize(vec_size);
        std::generate(vec.begin(), vec.end(), item_generator);
        client.PostArray(vec);
    }

    // Allocate target vectors
    std::vector<vector_type> target_vectors(num_vectors);
    for(auto &vec: target_vectors) {
        vec.reserve(vec_size);
    }
    auto array_ids = client.get_array_ids();

    // Preheat the connection
    for(std::size_t i = 0; i < num_preheat; ++i) {
        array_getter(target_vectors[i], array_ids[i]);
    }

    // Run the measurement
    auto start = std::chrono::high_resolution_clock::now();
#pragma omp parallel for
    for(std::size_t i = num_preheat; i < num_vectors; ++i) {
        array_getter(target_vectors[i], array_ids[i]);
    }
    auto stop = std::chrono::high_resolution_clock::now();
    int64_t duration = std::chrono::duration_cast<std::chrono::microseconds>(stop - start).count();

    // Check correctness
    for(std::size_t i = 0; i < num_vectors; ++i) {
        for(std::size_t j = 0; j < vec_size; ++j) {
            if(source_vectors[i][j] != target_vectors[i][j]) {
                std::cout << "(i, j)=(" << i << ", " << j << ")" << std::endl;
                std::cout <<source_vectors[i][j] << "!=" << target_vectors[i][j] << std::endl;
                throw std::runtime_error("Results do not match the source vector.");
            }
        }
    }
    client.DeleteArrays();
    return duration;
}

struct Measurement {
    int64_t runtime;
    std::size_t num_repetitions;
    std::size_t vec_size;
    std::size_t chunk_size;
    std::size_t type_size;
    std::string type_id;
    std::string method_id;
    std::string item_generator_id;
};

void print_measurement(Measurement m) {
    std::cout <<
    m.runtime << "," <<
    m.num_repetitions << "," <<
    m.vec_size << "," <<
    m.chunk_size << "," <<
    m.type_size << "," <<
    m.type_id << "," <<
    m.method_id << "," <<
    m.item_generator_id <<
    std::endl;
}

void print_measurement_header() {
    std::cout <<
    "runtime" << "," <<
    "num_repetitions" << "," <<
    "vec_size" << "," <<
    "chunk_size" << "," <<
    "type_size" << "," <<
    "type_id" << "," <<
    "method_id" << "," <<
    "item_generator_id" <<
    std::endl;
}

struct MeasurementParameters {
    std::size_t num_measurements;
    std::size_t num_repetitions_per_measurement;
    int64_t max_time_microseconds;
    std::size_t max_vec_size;
};

template<typename GrpcType>
void run_measurements_without_chunking(
    ArrayServiceClient<GrpcType>& client,
    std::function<void(typename TypesLookup<GrpcType>::vector_type&, const array_id_type)> array_getter,
    std::string method_id,
    const MeasurementParameters & measurement_params,
    std::function<typename TypesLookup<GrpcType>::data_type()> item_generator,
    std::string item_generator_id,
    std::size_t printed_chunk_size=0
) {
    auto type_id = TypesLookup<GrpcType>::type_id;
    using data_type = typename TypesLookup<GrpcType>::data_type;

    for(std::size_t vec_size = 1; vec_size <= measurement_params.max_vec_size; vec_size <<=1 ) {
        int64_t fastest_runtime = std::numeric_limits<int64_t>::max();
        for(std::size_t count = 0; count < measurement_params.num_measurements; ++count) {
            auto runtime = measure_runtime(
                client,
                array_getter,
                vec_size,
                measurement_params.num_repetitions_per_measurement,
                2,
                item_generator
            );
            fastest_runtime = std::min(runtime, fastest_runtime);
            print_measurement({
                runtime,
                measurement_params.num_repetitions_per_measurement,
                vec_size,
                printed_chunk_size,
                sizeof(data_type),
                std::string(type_id),
                method_id,
                item_generator_id
            });
        }
        if(fastest_runtime > measurement_params.max_time_microseconds) break;
    }
}

template<typename GrpcType>
void run_measurements_with_chunking(
    ArrayServiceClient<GrpcType>& client,
    std::function<void(typename TypesLookup<GrpcType>::vector_type&, const array_id_type, const std::size_t)> array_getter_with_chunking,
    std::string method_id,
    const MeasurementParameters & measurement_params,
    std::function<typename TypesLookup<GrpcType>::data_type()> item_generator,
    std::string item_generator_id
) {
    auto type_id = TypesLookup<GrpcType>::type_id;
    using data_type = typename TypesLookup<GrpcType>::data_type;

    for(std::size_t vec_size = 1; vec_size <= measurement_params.max_vec_size; vec_size <<= 1) {

        int64_t fastest_runtime = std::numeric_limits<int64_t>::max();
        for(std::size_t chunk_size = std::min(std::size_t(vec_size), std::size_t(1)<<11); chunk_size <= vec_size; chunk_size <<= 1) {
            auto array_getter = [&array_getter_with_chunking, &chunk_size](auto & vec, auto array_id){array_getter_with_chunking(vec, array_id, chunk_size);};
            for(std::size_t count = 0; count < measurement_params.num_measurements; ++count) {
                auto runtime = measure_runtime(
                    client,
                    array_getter,
                    vec_size,
                    measurement_params.num_repetitions_per_measurement,
                    2,
                    item_generator
                );
                fastest_runtime = std::min(runtime, fastest_runtime);
                print_measurement({
                    runtime,
                    measurement_params.num_repetitions_per_measurement,
                    vec_size,
                    chunk_size,
                    sizeof(data_type),
                    std::string(type_id),
                    method_id,
                    item_generator_id
                });
            }
        }
        if(fastest_runtime > measurement_params.max_time_microseconds) break;
    }
}

template<typename GrpcType>
void run_all_measurements(
    ArrayServiceClient<GrpcType>& client,
    const MeasurementParameters & measurement_params,
    std::function<typename TypesLookup<GrpcType>::data_type()> item_generator,
    std::string item_generator_id
) {
    using data_type = typename TypesLookup<GrpcType>::data_type;

    run_measurements_without_chunking(
        client,
        [&client](auto & target_vec, auto array_id){client.GetArray(target_vec, array_id);},
        "GetArray",
        measurement_params,
        item_generator,
        item_generator_id
    );
    run_measurements_without_chunking(
        client,
        [&client](auto & target_vec, auto array_id){client.GetArrayStreaming(target_vec, array_id);},
        "GetArrayStreaming",
        measurement_params,
        item_generator,
        item_generator_id
    );

    run_measurements_with_chunking(
        client,
        [&client](auto & target_vec, auto array_id, const std::size_t chunk_size){
            client.GetArrayChunked(target_vec, array_id, chunk_size);
        },
        "GetArrayChunked",
        measurement_params,
        item_generator,
        item_generator_id
    );
    run_measurements_with_chunking(
        client,
        [&client](auto & target_vec, auto array_id, const std::size_t chunk_size){
            client.GetArrayBinaryChunked(target_vec, array_id, chunk_size * sizeof(data_type));
        },
        "GetArrayBinaryChunked",
        measurement_params,
        item_generator,
        item_generator_id
    );
}

template<typename GrpcType>
void run_fixed_chunksize_measurements(
    ArrayServiceClient<GrpcType>& client,
    const MeasurementParameters & measurement_params,
    const std::size_t chunk_size,
    std::function<typename TypesLookup<GrpcType>::data_type()> item_generator,
    std::string item_generator_id
) {
    using data_type = typename TypesLookup<GrpcType>::data_type;

    run_measurements_without_chunking(
        client,
        [&client](auto & target_vec, auto array_id){client.GetArray(target_vec, array_id);},
        "GetArray",
        measurement_params,
        item_generator,
        item_generator_id
    );
    run_measurements_without_chunking(
        client,
        [&client](auto & target_vec, auto array_id){client.GetArrayStreaming(target_vec, array_id);},
        "GetArrayStreaming",
        measurement_params,
        item_generator,
        item_generator_id
    );

    run_measurements_without_chunking(
        client,
        [&client, &chunk_size](auto & target_vec, auto array_id){
            client.GetArrayChunked(target_vec, array_id, chunk_size);
        },
        "GetArrayChunked",
        measurement_params,
        item_generator,
        item_generator_id,
        chunk_size
    );
    run_measurements_without_chunking(
        client,
        [&client, &chunk_size](auto & target_vec, auto array_id){
            client.GetArrayBinaryChunked(target_vec, array_id, chunk_size * sizeof(data_type));
        },
        "GetArrayBinaryChunked",
        measurement_params,
        item_generator,
        item_generator_id,
        chunk_size
    );
}

} // end of namespace send_array
