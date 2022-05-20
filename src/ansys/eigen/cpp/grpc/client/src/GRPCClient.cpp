#include "GRPCClient.hpp"

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
    send_vector(writer, vec1);
    send_vector(writer, vec2);

    // Finish sending messages
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
    send_vector(writer, vec1);
    send_vector(writer, vec2);

    // Finish sending messages
    writer->WritesDone();
    ::grpc::Status status = writer->Finish();

    // Act upon its status.
    if (status.ok()) {
        std::cout
            << ">>>> Server vector dot product successful! Retrieving result."
            << std::endl;
        return deserialize_vector(reply.vector_as_chunk(), reply.vector_size(),
                                  reply.data_type())
            .at(0);

    } else {
        std::cout << ">>>> Request failed --> " << status.error_code() << ": "
                  << status.error_message() << std::endl;
        throw std::runtime_error("Error while executing 'multiply_vectors'.");
    }
}

std::vector<std::vector<double>> ansys::grpc::client::GRPCClient::add_matrices(
    const std::vector<std::vector<double>>& mat1,
    const std::vector<std::vector<double>>& mat2) {
    // Log the request
    std::cout << ">>>> Requesting matrix addition!" << std::endl;

    // Build the context, reply and request messages
    ::grpc::ClientContext context;
    grpcdemo::Matrix reply;

    // Create the writer for the sequenced/streamed RPC
    auto writer = _stub->AddMatrices(&context, &reply);

    // Write the two matrices
    send_matrix(writer, mat1);
    send_matrix(writer, mat2);

    // Finish sending messages
    writer->WritesDone();
    ::grpc::Status status = writer->Finish();

    // Act upon its status.
    if (status.ok()) {
        std::cout
            << ">>>> Server matrix addition successful! Retrieving matrix."
            << std::endl;
        return deserialize_matrix(reply.matrix_as_chunk(), reply.matrix_rows(),
                                  reply.matrix_cols(), reply.data_type());

    } else {
        std::cout << ">>>> Request failed --> " << status.error_code() << ": "
                  << status.error_message() << std::endl;
        throw std::runtime_error("Error while executing 'add_matrices'.");
    }
}

std::vector<std::vector<double>>
ansys::grpc::client::GRPCClient::multiply_matrices(
    const std::vector<std::vector<double>>& mat1,
    const std::vector<std::vector<double>>& mat2) {
    // Log the request
    std::cout << ">>>> Requesting matrix multiplication!" << std::endl;

    // Build the context, reply and request messages
    ::grpc::ClientContext context;
    grpcdemo::Matrix reply;

    // Create the writer for the sequenced/streamed RPC
    auto writer = _stub->MultiplyMatrices(&context, &reply);

    // Write the two matrices
    send_matrix(writer, mat1);
    send_matrix(writer, mat2);

    writer->WritesDone();
    ::grpc::Status status = writer->Finish();

    // Act upon its status.
    if (status.ok()) {
        std::cout << ">>>> Server matrix multiplication successful! Retrieving "
                     "matrix."
                  << std::endl;
        return deserialize_matrix(reply.matrix_as_chunk(), reply.matrix_rows(),
                                  reply.matrix_cols(), reply.data_type());

    } else {
        std::cout << ">>>> Request failed --> " << status.error_code() << ": "
                  << status.error_message() << std::endl;
        throw std::runtime_error("Error while executing 'multiply_matrices'.");
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
        // Init the row vector
        std::vector<double> row_vec{};
        row_vec.resize(cols);

        // Fill in the row vector
        for (int col_idx = 0; col_idx < cols; col_idx++) {
            memcpy(&row_vec[col_idx], ptr, step);
            ptr += step;
        }

        // Push the row vevctor
        matrix.push_back(row_vec);
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
        for (int col_idx = 0; col_idx < row_vec.size(); ++col_idx) {
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

void ansys::grpc::client::GRPCClient::send_vector(
    std::unique_ptr<::grpc::ClientWriter<grpcdemo::Vector>>& writer,
    const std::vector<double>& vector) {
    // Initialize the message
    grpcdemo::Vector request;

    // Fill in the message
    request.set_data_type(grpcdemo::DataType::DOUBLE);
    request.set_vector_size(vector.size());
    request.set_vector_as_chunk(serialize_vector(vector));

    // Write the message
    writer->Write(request);
}

void ansys::grpc::client::GRPCClient::send_matrix(
    std::unique_ptr<::grpc::ClientWriter<grpcdemo::Matrix>>& writer,
    const std::vector<std::vector<double>>& matrix) {
    // Initialize the message
    grpcdemo::Matrix request;

    // Fill in the message
    request.set_data_type(grpcdemo::DataType::DOUBLE);
    request.set_matrix_rows(matrix.size());
    request.set_matrix_cols(matrix.begin()->size());
    request.set_matrix_as_chunk(serialize_matrix(matrix));

    // Write the message
    writer->Write(request);
}

// ============================================================================
// ansys::grpc::client NAMESPACE METHODS
// ============================================================================
