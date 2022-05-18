#include "GRPCClient.hpp"

#include <grpcpp/grpcpp.h>

#include <iostream>

// ============================================================================
// GRPCClient PUBLIC METHODS
// ============================================================================

// GRPCClient Ctor. & Dtor.
// ----------------------------------------------------------------------------

ansys::grpc::client::GRPCClient::GRPCClient(const std::string host,
                                            const int port) {
    // Compile the host and port into the target url
    const std::string target = {host + ":" + std::to_string(port)};

    // Start by creating the associated channel. For this demo - Insecure
    // channel
    auto channel =
        ::grpc::CreateChannel(target, ::grpc::InsecureChannelCredentials());

    // Now, build the stub from the created channel
    _stub = grpcdemo::GRPCDemo::NewStub(channel);

    // Log the creation of the GRPCClient object
    std::cout << "GRPCClient object created." << std::endl;
}

ansys::grpc::client::GRPCClient::~GRPCClient() {
    // Start destroying the GRPCClient object
    std::cout << "GRPCClient object destroyed." << std::endl;
}

// GRPCClient Functionalities
// ----------------------------------------------------------------------------

void ansys::grpc::client::GRPCClient::request_greeting(
    const std::string& name) {
    // Log the request
    std::cout << ">>>> Requesting greeting for " << name << std::endl;

    // Build the context, reply and request messages
    ::grpc::ClientContext context;
    grpcdemo::HelloRequest request;
    grpcdemo::HelloReply reply;

    // Set the parameters of the request
    request.set_name(name);

    // Perform the actual RPC
    ::grpc::Status status = _stub->SayHello(&context, request, &reply);

    // Act upon its status.
    if (status.ok()) {
        std::cout << ">>>> Server answered --> " << reply.message()
                  << std::endl;
    } else {
        std::cout << ">>>> Request failed --> " << status.error_code() << ": "
                  << status.error_message() << std::endl;
        throw std::runtime_error("Error while executing 'request_greeting'.");
    }
}

std::vector<double> ansys::grpc::client::GRPCClient::flip_vector(
    const std::vector<double>& vec) {
    // Log the request
    std::cout << ">>>> Requesting vector flip!" << std::endl;

    // Build the context, reply and request messages
    ::grpc::ClientContext context;
    grpcdemo::Vector request;
    grpcdemo::Vector reply;

    // Set the parameters of the request
    request.set_data_type(grpcdemo::DataType::DOUBLE);
    request.set_vector_size(vec.size());
    request.set_vector_as_chunk(serialize_vector(vec));

    // Perform the actual RPC
    ::grpc::Status status = _stub->FlipVector(&context, request, &reply);

    // Act upon its status.
    if (status.ok()) {
        std::cout << ">>>> Server vector flip successful! Retrieving vector."
                  << std::endl;
        return deserialize_vector(reply.vector_as_chunk(), reply.vector_size(),
                                  reply.data_type());

    } else {
        std::cout << ">>>> Request failed --> " << status.error_code() << ": "
                  << status.error_message() << std::endl;
        throw std::runtime_error("Error while executing 'flip_vector'.");
    }
}

std::vector<double> ansys::grpc::client::GRPCClient::add_vectors(
    const std::vector<double>& vec1, const std::vector<double>& vec2) {
    // Log the request
    std::cout << ">>>> Requesting vector addition!" << std::endl;

    // Build the context, reply and request messages
    ::grpc::ClientContext context;
    grpcdemo::Vector reply;

    // Create the writer for the sequenced/streamed RPC
    auto writer = _stub->AddVectors(&context, &reply);

    // Write the two vectors
    grpcdemo::Vector request1;
    request1.set_data_type(grpcdemo::DataType::DOUBLE);
    request1.set_vector_size(vec1.size());
    request1.set_vector_as_chunk(serialize_vector(vec1));
    writer->Write(request1);

    grpcdemo::Vector request2;
    request2.set_data_type(grpcdemo::DataType::DOUBLE);
    request2.set_vector_size(vec2.size());
    request2.set_vector_as_chunk(serialize_vector(vec2));
    writer->Write(request2);

    writer->WritesDone();
    ::grpc::Status status = writer->Finish();

    // Act upon its status.
    if (status.ok()) {
        std::cout
            << ">>>> Server vector addition successful! Retrieving vector."
            << std::endl;
        return deserialize_vector(reply.vector_as_chunk(), reply.vector_size(),
                                  reply.data_type());

    } else {
        std::cout << ">>>> Request failed --> " << status.error_code() << ": "
                  << status.error_message() << std::endl;
        throw std::runtime_error("Error while executing 'add_vectors'.");
    }
}

double ansys::grpc::client::GRPCClient::multiply_vectors(
    const std::vector<double>& vec1, const std::vector<double>& vec2) {
    // Log the request
    std::cout << ">>>> Requesting vector dot product!" << std::endl;

    // Build the context, reply and request messages
    ::grpc::ClientContext context;
    grpcdemo::Vector reply;

    // Create the writer for the sequenced/streamed RPC
    auto writer = _stub->MultiplyVectors(&context, &reply);

    // Write the two vectors
    grpcdemo::Vector request1;
    request1.set_data_type(grpcdemo::DataType::DOUBLE);
    request1.set_vector_size(vec1.size());
    request1.set_vector_as_chunk(serialize_vector(vec1));
    writer->Write(request1);

    grpcdemo::Vector request2;
    request2.set_data_type(grpcdemo::DataType::DOUBLE);
    request2.set_vector_size(vec2.size());
    request2.set_vector_as_chunk(serialize_vector(vec2));
    writer->Write(request2);

    writer->WritesDone();
    ::grpc::Status status = writer->Finish();

    // Act upon its status.
    if (status.ok()) {
        std::cout
            << ">>>> Server vector dot product successful! Retrieving result."
            << std::endl;
        return deserialize_vector(reply.vector_as_chunk(), reply.vector_size(),
                                  reply.data_type()).at(0);

    } else {
        std::cout << ">>>> Request failed --> " << status.error_code() << ": "
                  << status.error_message() << std::endl;
        throw std::runtime_error("Error while executing 'multiply_vectors'.");
    }
}

// ============================================================================
// GRPCClient PRIVATE METHODS
// ============================================================================

std::vector<double> ansys::grpc::client::GRPCClient::deserialize_vector(
    const std::string& bytes, const int length, grpcdemo::DataType type) {
    // Get the step of the bytes array to interpret each type
    int step{0};
    switch (type) {
        case grpcdemo::DataType::DOUBLE:
            step = sizeof(double);
            break;
        case grpcdemo::DataType::INTEGER:
            step = sizeof(int);
            break;
        default:
            throw std::invalid_argument("Invalid Vector type!");
    }

    // Interpret the stream of bytes
    std::vector<double> vector{};
    vector.resize(length);

    // Turn into a const char*
    auto ptr = bytes.data();

    // Loop over the stream of bytes
    for (int idx = 0; idx < length; idx++) {
        memcpy(&vector[idx], ptr, step);
        ptr += step;
    }

    // Return the vector
    return vector;
}

std::string ansys::grpc::client::GRPCClient::serialize_vector(
    const std::vector<double>& vector) {
    // Initialize the serialized vector
    std::string vec_as_str{};

    // Loop over all vector elements
    for (int idx = 0; idx < vector.size(); ++idx) {
        // We will assume that all elements are of type double
        const unsigned char* ptr =
            reinterpret_cast<const unsigned char*>(&vector.at(idx));

        // Serialize!
        for (size_t i = 0; i < sizeof(double); ++i)
            vec_as_str.push_back(ptr[i]);
    }

    // Return the vector "serialized"
    return vec_as_str;
}

std::vector<std::vector<double>>
ansys::grpc::client::GRPCClient::deserialize_matrix(const std::string& bytes,
                                                    const int rows,
                                                    const int cols,
                                                    grpcdemo::DataType type) {
    // Get the step of the bytes array to interpret each type
    int step{0};
    switch (type) {
        case grpcdemo::DataType::DOUBLE:
            step = sizeof(double);
            break;
        case grpcdemo::DataType::INTEGER:
            step = sizeof(int);
            break;
        default:
            throw std::invalid_argument("Invalid Matrix type!");
    }

    // Interpret the stream of bytes
    std::vector<std::vector<double>> matrix{};

    // Turn into a const char*
    auto ptr = bytes.data();

    // Loop over the stream of bytes
    for (int row_idx = 0; row_idx < rows; row_idx++) {
        for (int col_idx = 0; col_idx < cols; col_idx++) {
            memcpy(&matrix[row_idx][col_idx], ptr, step);
            ptr += step;
        }
    }

    // Return the matrix
    return matrix;
}

std::string ansys::grpc::client::GRPCClient::serialize_matrix(
    const std::vector<std::vector<double>>& matrix) {
    // Initialize the serialized matrix
    std::string mat_as_str{};

    // Loop over all elements in the matrix: rows --> highest level
    for (int row_idx = 0; row_idx < matrix.size(); ++row_idx) {
        // Get the row vector
        const auto& row_vec = matrix.at(row_idx);

        // Loop over columns in the row vector
        for (int col_idx = 0; col_idx < matrix.size(); ++col_idx) {
            // We will assume that all elements are of type double
            const unsigned char* ptr =
                reinterpret_cast<const unsigned char*>(&row_vec[col_idx]);

            // Serialize!
            for (size_t i = 0; i < sizeof(double); ++i)
                mat_as_str.push_back(ptr[i]);
        }
    }

    // Return the matrix "serialized"
    return mat_as_str;
}

// ============================================================================
// ansys::grpc::client NAMESPACE METHODS
// ============================================================================
