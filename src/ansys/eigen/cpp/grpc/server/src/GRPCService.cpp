#include "GRPCService.hpp"

#include <exception>
#include <iostream>

// ============================================================================
// GRPCService PUBLIC METHODS
// ============================================================================

// GRPCService Ctor. & Dtor.
// ----------------------------------------------------------------------------

ansys::grpc::service::GRPCService::GRPCService() {
    // Start creating the GRPCService object
    std::cout << "GRPCService object created." << std::endl;
}

ansys::grpc::service::GRPCService::~GRPCService() {
    // Start destroying the GRPCService object
    std::cout << "GRPCService object destroyed." << std::endl;
}

// GRPCService Functionalities
// ----------------------------------------------------------------------------

::grpc::Status ansys::grpc::service::GRPCService::SayHello(
    ::grpc::ServerContext* context, const ::grpcdemo::HelloRequest* request,
    ::grpcdemo::HelloReply* response) {
    // Log event
    std::cout << "Greeting requested! Requested by " << request->name()
              << std::endl;

    // Define the response!
    response->set_message("Hello, " + request->name() + "!");
    return ::grpc::Status::OK;
}

::grpc::Status ansys::grpc::service::GRPCService::FlipVector(
    ::grpc::ServerContext* context, const ::grpcdemo::Vector* request,
    ::grpcdemo::Vector* response) {
    // Log event
    std::cout << "Vector flip requested!" << std::endl;

    // First, deserialize our vector into an Eigen::VectorXd object
    auto vec = deserialize_vector(request->vector_as_chunk(),
                                  request->vector_size(), request->data_type());

    // Flip the vector
    Eigen::VectorXd flip_vec = vec.reverse();

    // Send the response
    response->set_data_type(request->data_type());
    response->set_vector_size(request->vector_size());
    response->set_vector_as_chunk(serialize_vector(flip_vec));
    return ::grpc::Status::OK;
}

::grpc::Status ansys::grpc::service::GRPCService::AddVectors(
    ::grpc::ServerContext* context,
    ::grpc::ServerReader< ::grpcdemo::Vector>* reader,
    ::grpcdemo::Vector* response) {}

::grpc::Status ansys::grpc::service::GRPCService::MultiplyVectors(
    ::grpc::ServerContext* context,
    ::grpc::ServerReader< ::grpcdemo::Vector>* reader,
    ::grpcdemo::Vector* response) {}

::grpc::Status ansys::grpc::service::GRPCService::AddMatrices(
    ::grpc::ServerContext* context,
    ::grpc::ServerReader< ::grpcdemo::Matrix>* reader,
    ::grpcdemo::Matrix* response) {}

::grpc::Status ansys::grpc::service::GRPCService::MultiplyMatrices(
    ::grpc::ServerContext* context,
    ::grpc::ServerReader< ::grpcdemo::Matrix>* reader,
    ::grpcdemo::Matrix* response) {}

// ============================================================================
// GRPCService PRIVATE METHODS
// ============================================================================

Eigen::VectorXd ansys::grpc::service::GRPCService::deserialize_vector(
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

    // Turn into a const char*
    auto ptr = bytes.data();
    int idx{0};

    // Interpret the stream of bytes
    Eigen::VectorXd vector{};
    vector.resize(length);
    while (idx < length) {
        // Decode first (depending on data type)
        switch (type) {
            case grpcdemo::DataType::DOUBLE:
                vector[idx] = std::atof(ptr);
                break;
            case grpcdemo::DataType::INTEGER:
                vector[idx] = std::atoi(ptr);
                break;
        }

        // Advance to next position
        ptr += step;
        idx++;
    }

    return vector;
}

std::string ansys::grpc::service::GRPCService::serialize_vector(
    const Eigen::VectorXd& vector) {
    std::string vec_as_str{};

    for (int idx = 0; idx < vector.size(); ++idx) {
        // We will assume that all elements are of type double
        const unsigned char* ptr =
            reinterpret_cast<const unsigned char*>(&vector[idx]);
        for (size_t i = 0; i < sizeof(double); ++i)
            vec_as_str.push_back(ptr[i]);
    }

    return vec_as_str;
}

Eigen::MatrixXd ansys::grpc::service::GRPCService::deserialize_matrix(
    const std::string& bytes, const int rows, const int cols,
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

    // Turn into a const char*
    auto ptr = bytes.data();
    int idx{0};

    // Interpret the stream of bytes
    Eigen::MatrixXd matrix{};
    matrix.resize(rows, cols);
    int row_idx{0}, col_idx{0};

    while (idx < rows * cols) {
        // Decode first (depending on data type)
        switch (type) {
            case grpcdemo::DataType::DOUBLE:
                matrix(row_idx, col_idx) = std::atof(ptr);
                break;
            case grpcdemo::DataType::INTEGER:
                matrix(row_idx, col_idx) = std::atoi(ptr);
                break;
        }

        // Move the row/col indices
        if (col_idx < cols) {
            col_idx++;
        } else {
            col_idx = 0;
            row_idx++;
        }

        // Advance to next position
        ptr += step;
        idx++;
    }

    return matrix;
}

std::string ansys::grpc::service::GRPCService::serialize_matrix(
    const Eigen::MatrixXd& matrix) {
    std::string mat_as_str{};

    for (int row_idx = 0; row_idx < matrix.rows(); ++row_idx) {
        for (int col_idx = 0; col_idx < matrix.cols(); ++col_idx) {
            // We will assume that all elements are of type double
            const unsigned char* ptr = reinterpret_cast<const unsigned char*>(
                &matrix(row_idx, col_idx));
            for (size_t i = 0; i < sizeof(double); ++i)
                mat_as_str.push_back(ptr[i]);
        }
    }

    return mat_as_str;
}

// ============================================================================
// ansys::grpc::server NAMESPACE METHODS
// ============================================================================
