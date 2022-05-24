#include "GRPCService.hpp"

#include <exception>
#include <iostream>

/**
 * @brief Maximum length for the chunks in the messages: 3MB.
 */
constexpr int MAX_CHUNK_LENGTH = 1024 * 1024 * 3;

/**
 * @brief Maximum elements for a double vector/matrix.
 */
constexpr int MAX_ELEMS_LENGTH = MAX_CHUNK_LENGTH / 8;

// ============================================================================
// GRPCService PUBLIC METHODS
// ============================================================================

// GRPCService Ctor. & Dtor.
// ----------------------------------------------------------------------------

ansys::grpc::service::GRPCService::GRPCService(const bool debug_log)
    : _debug_log(debug_log) {
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
    std::cout << ">>>> Greeting requested! Requested by " << request->name()
              << std::endl;

    // Define the response!
    response->set_message("Hello, " + request->name() + "!");
    return ::grpc::Status::OK;
}

::grpc::Status ansys::grpc::service::GRPCService::FlipVector(
    ::grpc::ServerContext* context,
    ::grpc::ServerReaderWriter<::grpcdemo::Vector, ::grpcdemo::Vector>*
        stream) {
    // Log event
    std::cout << ">>>> Vector flip requested!" << std::endl;

    // First, deserialize our vector into an Eigen::VectorXd object
    auto vec = receive_vectors(stream, context).at(0);

    if (_debug_log) {
        std::cout << ">>>> Incoming Vector: " << vec.transpose() << std::endl;
    }

    // Flip the vector
    Eigen::VectorXd flip_vec = vec.reverse();

    // Log the result
    if (_debug_log) {
        std::cout << ">>>> Result of vector flip: " << flip_vec.transpose()
                  << std::endl;
    }

    // Send the response
    send_vector(stream, context, flip_vec);

    // If everything went fine... send OK response
    return ::grpc::Status::OK;
}

::grpc::Status ansys::grpc::service::GRPCService::AddVectors(
    ::grpc::ServerContext* context,
    ::grpc::ServerReaderWriter<::grpcdemo::Vector, ::grpcdemo::Vector>*
        stream) {
    // Log event
    std::cout << ">>>> Vector addition requested!" << std::endl;

    // First, deserialize our vectors into Eigen::VectorXd objects
    auto vecs = receive_vectors(stream, context);

    // Initialize our result variable
    Eigen::VectorXd result{};

    // Loop over the transmitted vectors
    for (const auto& vec : vecs) {
        // Log involved vectors if desired
        if (_debug_log) {
            std::cout << ">>>> Incoming Vector: " << vec.transpose()
                      << std::endl;
        }

        // Perform some checks
        if (result.size() == 0) {
            // This means that our vector has not been initialized yet!
            result = vec;
        } else if (vec.size() != result.size()) {
            // This means that the incoming vectors have different sizes... This
            // is not supported!
            std::string error{
                ">>>> ERR: Incoming vectors are of different sizes."};
            std::cout << error << std::endl;
            return ::grpc::Status(::grpc::StatusCode::CANCELLED, error);
        } else {
            // Otherwise, everything is OK... Perform the addition!
            result += vec;
        }
    }

    // Log the result
    if (_debug_log) {
        std::cout << ">>>> Result of addition: " << result.transpose()
                  << std::endl;
    }

    // Send the response
    send_vector(stream, context, result);

    // If everything went fine... send OK response
    return ::grpc::Status::OK;
}

::grpc::Status ansys::grpc::service::GRPCService::MultiplyVectors(
    ::grpc::ServerContext* context,
    ::grpc::ServerReaderWriter<::grpcdemo::Vector, ::grpcdemo::Vector>*
        stream) {
    // Log event
    std::cout << ">>>> Vector dot product requested!" << std::endl;

    // First, deserialize our vectors into Eigen::VectorXd objects
    auto vecs = receive_vectors(stream, context);

    // Perform the dot product if possible
    double dot_product;
    if (vecs.size() != 2) {
        // This means that the incoming vectors have different sizes... This
        // is not supported!
        std::string error{
            ">>>> ERR: Innvalid amount of vectors for dot product."};
        std::cout << error << std::endl;
        return ::grpc::Status(::grpc::StatusCode::CANCELLED, error);
    } else if (vecs.at(0).size() != vecs.at(1).size()) {
        // This means that the incoming vectors have different sizes... This
        // is not supported!
        std::string error{">>>> ERR: Incoming vectors are of different sizes."};
        std::cout << error << std::endl;
        return ::grpc::Status(::grpc::StatusCode::CANCELLED, error);
    } else {
        // Log involved vectors if desired
        if (_debug_log) {
            std::cout << ">>>> Incoming Vector: " << vecs.at(0).transpose()
                      << std::endl;
            std::cout << ">>>> Incoming Vector: " << vecs.at(1).transpose()
                      << std::endl;
        }

        // Perform the dot product
        dot_product = vecs.at(0).dot(vecs.at(1));
    }

    // Build the result Eigen::VectorXd
    Eigen::VectorXd result{};
    result.resize(1);
    result << dot_product;

    // Log the result
    if (_debug_log) {
        std::cout << ">>>> Result of dot product: " << std::endl;
        std::cout << result << std::endl;
    }

    // Send the response
    send_vector(stream, context, result);

    // If everything went fine... send OK response
    return ::grpc::Status::OK;
}

::grpc::Status ansys::grpc::service::GRPCService::AddMatrices(
    ::grpc::ServerContext* context,
    ::grpc::ServerReaderWriter<::grpcdemo::Matrix, ::grpcdemo::Matrix>*
        stream) {
    // Log event
    std::cout << ">>>> Matrix addition requested!" << std::endl;

    // First, deserialize our matrices into Eigen::MatrixXd objects
    auto mats = receive_matrices(stream, context);

    // Initialize our result variable
    Eigen::MatrixXd result{};

    // Loop over the transmitted matrices
    for (const auto& mat : mats) {
        // Log incoming matrices if desired
        if (_debug_log) {
            std::cout << ">>>> Incoming Matrix: " << std::endl;
            std::cout << mat << std::endl;
        }

        // Perform some checks
        if (result.size() == 0) {
            // This means that our matrix has not been initialized yet!
            result = mat;
        } else if (mat.rows() != result.rows() || mat.cols() != result.cols()) {
            // This means that the incoming matrices have different sizes...
            // This is not supported!
            std::string error{
                ">>>> ERR: Incoming matrices are of different sizes."};
            std::cout << error << std::endl;
            return ::grpc::Status(::grpc::StatusCode::CANCELLED, error);
        } else {
            // Otherwise, everything is OK... Perform the addition!
            result += mat;
        }
    }

    // Log the result
    if (_debug_log) {
        std::cout << ">>>> Resulting Matrix: " << std::endl;
        std::cout << result << std::endl;
    }

    // Send the response
    send_matrix(stream, context, result);

    // If everything went fine... send OK response
    return ::grpc::Status::OK;
}

::grpc::Status ansys::grpc::service::GRPCService::MultiplyMatrices(
    ::grpc::ServerContext* context,
    ::grpc::ServerReaderWriter<::grpcdemo::Matrix, ::grpcdemo::Matrix>*
        stream) {
    // Log event
    std::cout << ">>>> Matrix multiplication requested!" << std::endl;

    // First, deserialize our matrices into Eigen::MatrixXd objects
    auto mats = receive_matrices(stream, context);

    // Initialize our result variable
    Eigen::MatrixXd result{};

    // Loop over the transmitted matrices
    for (const auto& mat : mats) {
        // Log incoming matrices if desired
        if (_debug_log) {
            std::cout << ">>>> Incoming Matrix: " << std::endl;
            std::cout << mat << std::endl;
        }

        // Perform some checks
        if (result.size() == 0) {
            // This means that our matrix has not been initialized yet!
            result = mat;
        } else if (mat.rows() != result.cols() || mat.cols() != result.rows()) {
            // This means that the incoming matrices have incompatible sizes...
            // This is not supported!
            std::string error{
                ">>>> ERR: Incoming matrices are of incompatible sizes."};
            std::cout << error << std::endl;
            return ::grpc::Status(::grpc::StatusCode::CANCELLED, error);
        } else {
            // Otherwise, everything is OK... Perform the multiplication!
            result *= mat;
        }
    }

    // Log the result
    if (_debug_log) {
        std::cout << ">>>> Resulting Matrix: " << std::endl;
        std::cout << result << std::endl;
    }

    // Send the response
    send_matrix(stream, context, result);

    // If everything went fine... send OK response
    return ::grpc::Status::OK;
}

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

    // Interpret the stream of bytes
    Eigen::VectorXd vector{};
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

std::string ansys::grpc::service::GRPCService::serialize_vector(
    const Eigen::VectorXd& vector, const int start, const int end) {
    // Initialize the serialized vector
    std::string vec_as_str{};

    // Loop over all vector elements
    for (int idx = start; idx < end; ++idx) {
        // We will assume that all elements are of type double
        const unsigned char* ptr =
            reinterpret_cast<const unsigned char*>(&vector[idx]);

        // Serialize!
        for (size_t i = 0; i < sizeof(double); ++i)
            vec_as_str.push_back(ptr[i]);
    }

    // Return the vector "serialized"
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

    // Interpret the stream of bytes
    Eigen::MatrixXd matrix{};
    matrix.resize(rows, cols);

    // Turn into a const char*
    auto ptr = bytes.data();

    // Loop over the stream of bytes
    for (int row_idx = 0; row_idx < rows; row_idx++) {
        for (int col_idx = 0; col_idx < cols; col_idx++) {
            memcpy(&matrix(row_idx, col_idx), ptr, step);
            ptr += step;
        }
    }

    // Return the matrix
    return matrix;
}

std::string ansys::grpc::service::GRPCService::serialize_matrix(
    const Eigen::MatrixXd& matrix, const int start, const int end) {
    // Initialize the serialized matrix
    std::string mat_as_str{};

    // Loop over all elements in the matrix: rows --> highest level
    for (int row_idx = start; row_idx < end; ++row_idx) {
        for (int col_idx = 0; col_idx < matrix.cols(); ++col_idx) {
            // We will assume that all elements are of type double
            const unsigned char* ptr = reinterpret_cast<const unsigned char*>(
                &matrix(row_idx, col_idx));

            // Serialize!
            for (size_t i = 0; i < sizeof(double); ++i)
                mat_as_str.push_back(ptr[i]);
        }
    }

    // Return the matrix "serialized"
    return mat_as_str;
}

std::vector<Eigen::VectorXd> ansys::grpc::service::GRPCService::receive_vectors(
    ::grpc::ServerReaderWriter<grpcdemo::Vector, grpcdemo::Vector>*
        reader_writer,
    ::grpc::ServerContext* context) {
    // Get the metadata
    auto md = context->client_metadata();

    // Determine how many full Vector messages we are expecting
    auto expected_vectors = std::atoi(md.find("full-vectors")->second.data());
    std::vector<Eigen::VectorXd> result_vectors{};

    // Now, let us process vector by vector
    for (int vec_i = 1; vec_i <= expected_vectors; ++vec_i) {
        // Find the expected amount of messages for the full Vector
        auto expected_messages =
            std::atoi(md.find("vec" + std::to_string(vec_i) + "-messages")
                          ->second.data());

        // Once the server has processed the metadata for this full Vector, let
        // us deserialize it
        grpcdemo::Vector request;

        // Depending on whether it is a multi-message Vector or a single
        // message, proceed as defined
        if (expected_messages == 1) {
            // Read the single message
            reader_writer->Read(&request);

            // Deserialize the vector
            auto vec =
                deserialize_vector(request.vector_as_chunk(),
                                   request.vector_size(), request.data_type());

            // Append the deserialized vector to the resulting std::vector
            result_vectors.push_back(vec);

        } else if (expected_messages > 1) {
            // Multiple messages to be processed -- Get the vector elements per
            // message / except for the last message, this has to be read from
            // the message information: vector_size
            std::vector<int> vector_sizes{};
            for (int i = 1; i < expected_messages; i++) {
                vector_sizes.push_back(MAX_ELEMS_LENGTH);
            }

            // Initialize certain variables
            Eigen::VectorXd glued_vector{};

            // Read all incoming messages to define the full Vector message
            for (int msg = 0; msg < expected_messages; msg++) {
                // Read the request
                reader_writer->Read(&request);

                // Check if it is the first message processed of the chunk
                if (msg == 0) {
                    // First time we are reading the vectors... Load the elems
                    // to be read in the final message!
                    vector_sizes.push_back(request.vector_size() -
                                           (expected_messages - 1) *
                                               MAX_ELEMS_LENGTH);
                }

                // Deserialize the incoming vector chunk
                auto aux_vector = deserialize_vector(request.vector_as_chunk(),
                                                     vector_sizes.at(msg),
                                                     request.data_type());

                // Append the aux_vector to the glued_vector
                Eigen::VectorXd tmp_vector = glued_vector;
                glued_vector.resize(tmp_vector.size() + aux_vector.size());
                glued_vector << tmp_vector, aux_vector;
            }

            // Once all partial messages have been processed, append!
            result_vectors.push_back(glued_vector);
        }
    }

    // Finally return the results vector
    return result_vectors;
}

std::vector<Eigen::MatrixXd>
ansys::grpc::service::GRPCService::receive_matrices(
    ::grpc::ServerReaderWriter<grpcdemo::Matrix, grpcdemo::Matrix>*
        reader_writer,
    ::grpc::ServerContext* context) {
    // Get the metadata
    auto md = context->client_metadata();

    // Determine how many full Matrix messages we are expecting
    auto expected_matrices = std::atoi(md.find("full-matrices")->second.data());
    std::vector<Eigen::MatrixXd> result_matrices{};

    // Now, let us process matrix by matrix
    for (int mat_i = 1; mat_i <= expected_matrices; ++mat_i) {
        // Find the expected amount of messages for the full Matrix
        auto expected_messages =
            std::atoi(md.find("mat" + std::to_string(mat_i) + "-messages")
                          ->second.data());

        // Once the server has processed the metadata for this full Vector, let
        // us deserialize it
        grpcdemo::Matrix request;

        // Depending on whether it is a multi-message Matrix or a single
        // message, proceed as defined
        if (expected_messages == 1) {
            // Read the single message
            reader_writer->Read(&request);

            // Deserialize the matrix
            auto mat = deserialize_matrix(
                request.matrix_as_chunk(), request.matrix_rows(),
                request.matrix_cols(), request.data_type());

            // Append the deserialized matrix to the resulting std::vector
            result_matrices.push_back(mat);

        } else if (expected_messages > 1) {
            // Initialize certain variables
            Eigen::MatrixXd glued_matrix{};

            // Multiple messages to be processed -- Get the matrix rows per
            // message / except for the last message, this has to be read from
            // the message information: matrix_rows
            std::vector<int> matrix_sizes{};

            // Read all incoming messages to define the full Matrix message
            for (int msg = 0; msg < expected_messages; msg++) {
                // Read the request
                reader_writer->Read(&request);

                // Check if it is the first message processed of the chunk
                if (msg == 0) {
                    // First time we are reading the matrices... Load the elems
                    // to be read in the message!
                    int max_rows_per_message =
                        MAX_ELEMS_LENGTH / request.matrix_cols();

                    for (int i = 1; i < expected_messages; i++) {
                        matrix_sizes.push_back(max_rows_per_message);
                    }

                    matrix_sizes.push_back(request.matrix_rows() -
                                           (expected_messages - 1) *
                                               max_rows_per_message);
                }

                // Deserialize the incoming matrix chunk
                auto aux_matrix = deserialize_matrix(
                    request.matrix_as_chunk(), matrix_sizes.at(msg),
                    request.matrix_cols(), request.data_type());

                // Append the aux_matrix to the glued_matrix
                Eigen::MatrixXd tmp_matrix = glued_matrix;
                glued_matrix.resize(tmp_matrix.rows() + aux_matrix.rows(),
                                    tmp_matrix.cols());
                glued_matrix << tmp_matrix, aux_matrix;
            }

            // Once all partial messages have been processed, append!
            result_matrices.push_back(glued_matrix);
        }
    }

    // Finally return the results matrix
    return result_matrices;
}

void ansys::grpc::service::GRPCService::send_vector(
    ::grpc::ServerReaderWriter<grpcdemo::Vector, grpcdemo::Vector>*
        reader_writer,
    ::grpc::ServerContext* context, const Eigen::VectorXd& vector) {
    // Process vector size
    int size_vec = vector.size();

    // Init the amount of chunks needed for the Vector to be transmitted
    std::vector<int> chunk_steps{};

    // If our vec size exceed the message max... split it!
    if (size_vec > MAX_ELEMS_LENGTH) {
        // Find out how many messages we will need (bulk value)
        int messages_bulk = size_vec / MAX_ELEMS_LENGTH;

        // Check the remainder! (if !=0, an extra message is needed)
        int remainder = size_vec % MAX_ELEMS_LENGTH;

        // Specify the indices up to which each message will cast
        for (int i = 1; i <= messages_bulk; i++) {
            chunk_steps.push_back(MAX_ELEMS_LENGTH * i);
        }

        // Consider the remainder as the final message
        if (remainder != 0) chunk_steps.push_back(size_vec);

    } else {
        // Otherwise... single message!
        chunk_steps.push_back(size_vec);
    }

    // Let us create the metadata for our response
    context->AddInitialMetadata("full-vectors", std::to_string(1));
    context->AddInitialMetadata("vec1-messages",
                                std::to_string(chunk_steps.size()));

    // Loop over the needed chunks --> This will define how many Vector messages
    // are needed for casting the entire Vector message
    int processed_idx{0};
    for (int chunk_end_idx : chunk_steps) {
        // Initialize the message
        grpcdemo::Vector request;

        // Fill in the message
        request.set_data_type(grpcdemo::DataType::DOUBLE);
        request.set_vector_size(size_vec);
        request.set_vector_as_chunk(
            serialize_vector(vector, processed_idx, chunk_end_idx));

        // Write the message
        reader_writer->Write(request);

        // Update the processed idx
        processed_idx += chunk_end_idx;
    }
}

void ansys::grpc::service::GRPCService::send_matrix(
    ::grpc::ServerReaderWriter<grpcdemo::Matrix, grpcdemo::Matrix>*
        reader_writer,
    ::grpc::ServerContext* context, const Eigen::MatrixXd& matrix) {
    // Process matrix size
    int rows_mat = matrix.rows();
    int cols_mat = matrix.cols();
    int elem_mat = rows_mat * cols_mat;

    // Init the amount of chunks needed for the Matrix to be transmitted
    std::vector<int> chunk_steps{};

    // If our vec size exceed the message max... split it!
    if (elem_mat > MAX_ELEMS_LENGTH) {
        // Knowing the amount of columns, we will transmit full rows only. This
        // leaves us with the maximum amount of rows to be transmitted in one
        // same message...
        int max_rows_per_message = MAX_ELEMS_LENGTH / cols_mat;

        // Find out how many messages we will need (bulk value)
        int messages_bulk = rows_mat / max_rows_per_message;

        // Check the remainder! (if !=0, an extra message is needed)
        int remainder = rows_mat % max_rows_per_message;

        // Specify the indices (i.e. row) up to which each message will cast
        for (int i = 1; i <= messages_bulk; i++) {
            chunk_steps.push_back(max_rows_per_message * i);
        }

        // Consider the remainder as the final message
        if (remainder != 0) chunk_steps.push_back(rows_mat);

    } else {
        // Otherwise... single message!
        chunk_steps.push_back(rows_mat);
    }

    // Let us create the metadata for our response
    context->AddInitialMetadata("full-matrices", std::to_string(1));
    context->AddInitialMetadata("mat1-messages",
                                std::to_string(chunk_steps.size()));

    // Loop over the needed chunks --> This will define how many Matrix messages
    // are needed for casting the entire Matrix message
    int processed_idx{0};
    for (int chunk_end_idx : chunk_steps) {
        // Initialize the message
        grpcdemo::Matrix request;

        // Fill in the message
        request.set_data_type(grpcdemo::DataType::DOUBLE);
        request.set_matrix_rows(rows_mat);
        request.set_matrix_cols(cols_mat);
        request.set_matrix_as_chunk(
            serialize_matrix(matrix, processed_idx, chunk_end_idx));

        // Write the message
        reader_writer->Write(request);

        // Update the processed idx
        processed_idx += chunk_end_idx;
    }
}
// ============================================================================
// ansys::grpc::server NAMESPACE METHODS
// ============================================================================
