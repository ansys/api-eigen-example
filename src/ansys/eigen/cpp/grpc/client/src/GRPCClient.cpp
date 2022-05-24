#include "GRPCClient.hpp"

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
// GRPCClient PUBLIC METHODS
// ============================================================================

// GRPCClient Ctor. & Dtor.
// ----------------------------------------------------------------------------

ansys::grpc::client::GRPCClient::GRPCClient(const std::string host,
                                            const int port,
                                            const bool debug_log)
    : _debug_log(debug_log) {
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
        if (_debug_log) {
            std::cout << ">>>> Server answered --> " << reply.message()
                      << std::endl;
        }
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

    // Build the context
    ::grpc::ClientContext context;

    // Define the metadata and the amount of chunks for each Vector
    // We get an std::vector<std::vector<int>> were each complete Vector message
    // is an entry of the outermost vector, and the innermost vector contains
    // information on the indices where the cuts are made
    //
    auto chunks = define_vecstream_metadata(&context, vec);

    // Create the writer for the sequenced/streamed RPC
    auto reader_writer = _stub->FlipVector(&context);

    // Write the vector
    send_vector(reader_writer, vec, chunks.at(0));

    // Finish sending messages
    reader_writer->WritesDone();

    // Wait for the server's metadata to be received
    reader_writer->WaitForInitialMetadata();

    // Process the server response
    auto result = receive_vector(reader_writer, &context);

    // Finalize streaming
    ::grpc::Status status = reader_writer->Finish();

    // Act upon its status.
    if (status.ok()) {
        if (_debug_log) {
            std::cout
                << ">>>> Server vector flip successful! Retrieving vector."
                << std::endl;
        }
        return result;

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

    // Build the context
    ::grpc::ClientContext context;

    // Define the metadata and the amount of chunks for each Vector
    // We get an std::vector<std::vector<int>> were each complete Vector message
    // is an entry of the outermost vector, and the innermost vector contains
    // information on the indices where the cuts are made
    //
    auto chunks = define_vecstream_metadata(&context, vec1, vec2);

    // Create the writer for the sequenced/streamed RPC
    auto reader_writer = _stub->AddVectors(&context);

    // Write the two vectors
    send_vector(reader_writer, vec1, chunks.at(0));
    send_vector(reader_writer, vec2, chunks.at(1));

    // Finish sending messages
    reader_writer->WritesDone();

    // Wait for the server's metadata to be received
    reader_writer->WaitForInitialMetadata();

    // Process the server response
    auto result = receive_vector(reader_writer, &context);

    // Finalize streaming
    ::grpc::Status status = reader_writer->Finish();

    // Act upon its status.
    if (status.ok()) {
        if (_debug_log) {
            std::cout
                << ">>>> Server vector addition successful! Retrieving vector."
                << std::endl;
        }
        return result;

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

    // Build the context
    ::grpc::ClientContext context;

    // Define the metadata and the amount of chunks for each Vector
    // We get an std::vector<std::vector<int>> were each complete Vector message
    // is an entry of the outermost vector, and the innermost vector contains
    // information on the indices where the cuts are made
    //
    auto chunks = define_vecstream_metadata(&context, vec1, vec2);

    // Create the writer for the sequenced/streamed RPC
    auto reader_writer = _stub->MultiplyVectors(&context);

    // Write the two vectors
    send_vector(reader_writer, vec1, chunks.at(0));
    send_vector(reader_writer, vec2, chunks.at(1));

    // Finish sending messages
    reader_writer->WritesDone();

    // Wait for the server's metadata to be received
    reader_writer->WaitForInitialMetadata();

    // Process the server response
    auto result = receive_vector(reader_writer, &context);

    // Finalize streaming
    ::grpc::Status status = reader_writer->Finish();

    // Act upon its status.
    if (status.ok()) {
        if (_debug_log) {
            std::cout << ">>>> Server vector dot product successful! "
                         "Retrieving result."
                      << std::endl;
        }
        return result.at(0);

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

    // Build the context
    ::grpc::ClientContext context;

    // Define the metadata and the amount of chunks for each Matrix
    // We get an std::vector<std::vector<int>> were each complete Matrix message
    // is an entry of the outermost vector, and the innermost vector contains
    // information on the indices where the cuts are made
    //
    auto chunks = define_matstream_metadata(&context, mat1, mat2);

    // Create the writer for the sequenced/streamed RPC
    auto reader_writer = _stub->AddMatrices(&context);

    // Write the two matrices
    send_matrix(reader_writer, mat1, chunks.at(0));
    send_matrix(reader_writer, mat2, chunks.at(1));

    // Finish sending messages
    reader_writer->WritesDone();

    // Wait for the server's metadata to be received
    reader_writer->WaitForInitialMetadata();

    // Process the server response
    auto result = receive_matrix(reader_writer, &context);

    // Finalize streaming
    ::grpc::Status status = reader_writer->Finish();

    // Act upon its status.
    if (status.ok()) {
        if (_debug_log) {
            std::cout
                << ">>>> Server matrix addition successful! Retrieving matrix."
                << std::endl;
        }
        return result;

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

    // Build the context
    ::grpc::ClientContext context;

    // Define the metadata and the amount of chunks for each Matrix
    // We get an std::vector<std::vector<int>> were each complete Matrix message
    // is an entry of the outermost vector, and the innermost vector contains
    // information on the indices where the cuts are made
    //
    auto chunks = define_matstream_metadata(&context, mat1, mat2);

    // Create the writer for the sequenced/streamed RPC
    auto reader_writer = _stub->MultiplyMatrices(&context);

    // Write the two matrices
    send_matrix(reader_writer, mat1, chunks.at(0));
    send_matrix(reader_writer, mat2, chunks.at(1));

    // Finish sending messages
    reader_writer->WritesDone();

    // Wait for the server's metadata to be received
    reader_writer->WaitForInitialMetadata();

    // Process the server response
    auto result = receive_matrix(reader_writer, &context);

    // Finalize streaming
    ::grpc::Status status = reader_writer->Finish();

    // Act upon its status.
    if (status.ok()) {
        if (_debug_log) {
            std::cout
                << ">>>> Server matrix multiplication successful! Retrieving "
                   "matrix."
                << std::endl;
        }
        return result;

    } else {
        std::cout << ">>>> Request failed --> " << status.error_code() << ": "
                  << status.error_message() << std::endl;
        throw std::runtime_error("Error while executing 'multiply_matrices'.");
    }
}

// ============================================================================
// GRPCClient PRIVATE METHODS
// ============================================================================

std::vector<std::vector<int>>
ansys::grpc::client::GRPCClient::define_vecstream_metadata(
    ::grpc::ClientContext* context, const std::vector<double>& vec1,
    const std::vector<double>& vec2) {
    // Initialize the output information
    std::vector<std::vector<int>> chunk_info{};

    // Check whether we are sending a single vector request (i.e. flip_vector)
    // or multiple...
    if (vec2.empty()) {
        context->AddMetadata("full-vectors", std::to_string(1));

        // Process vectors
        auto chunk1 = set_vector_metadata(context, vec1, "vec1");

        // Return all message chunks
        return std::vector<std::vector<int>>{chunk1};
    } else {
        context->AddMetadata("full-vectors", std::to_string(2));

        // Process vectors
        auto chunk1 = set_vector_metadata(context, vec1, "vec1");
        auto chunk2 = set_vector_metadata(context, vec2, "vec2");

        // Return all message chunks
        return std::vector<std::vector<int>>{chunk1, chunk2};
    }
}

std::vector<int> ansys::grpc::client::GRPCClient::set_vector_metadata(
    ::grpc::ClientContext* context, const std::vector<double>& vec,
    const std::string& vec_name) {
    // Process vector size
    int size_vec = vec.size();

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

    // Add the number of messages for Vector
    context->AddMetadata(vec_name + "-messages",
                         std::to_string(chunk_steps.size()));

    // Return the chunked steps
    return chunk_steps;
}

std::vector<std::vector<int>>
ansys::grpc::client::GRPCClient::define_matstream_metadata(
    ::grpc::ClientContext* context,
    const std::vector<std::vector<double>>& mat1,
    const std::vector<std::vector<double>>& mat2) {
    // Initialize the output information
    std::vector<std::vector<int>> chunk_info{};

    // For matrices, we will always be sending two matrices
    context->AddMetadata("full-matrices", std::to_string(2));

    // Process vectors
    auto chunk1 = set_matrix_metadata(context, mat1, "mat1");
    auto chunk2 = set_matrix_metadata(context, mat2, "mat2");

    // Return all message chunks
    return std::vector<std::vector<int>>{chunk1, chunk2};
}

std::vector<int> ansys::grpc::client::GRPCClient::set_matrix_metadata(
    ::grpc::ClientContext* context, const std::vector<std::vector<double>>& mat,
    const std::string& mat_name) {
    // Process matrix size: rows & cols. We will assume that all rows have the
    // same dimensions! It's kind of the deal with matrices =)
    int rows_mat = mat.size();
    int cols_mat = mat.begin()->size();
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

    // Add the number of messages for Matrix
    context->AddMetadata(mat_name + "-messages",
                         std::to_string(chunk_steps.size()));

    // Return the chunked steps
    return chunk_steps;
}

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
    const std::vector<double>& vector, const int start, const int end) {
    // Initialize the serialized vector
    std::string vec_as_str{};

    // Loop over all vector elements
    for (int idx = start; idx < end; ++idx) {
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
    const std::vector<std::vector<double>>& matrix, const int start,
    const int end) {
    // Initialize the serialized matrix
    std::string mat_as_str{};

    // Loop over all elements in the matrix: rows --> highest level
    for (int row_idx = start; row_idx < end; ++row_idx) {
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
    std::unique_ptr<::grpc::ClientReaderWriter<
        grpcdemo::Vector, grpcdemo::Vector>>& reader_writer,
    const std::vector<double>& vector, const std::vector<int>& chunks) {
    // Loop over the needed chunks --> This will define how many Vector messages
    // are needed for casting the entire Vector message
    int processed_idx{0};
    for (int chunk_end_idx : chunks) {
        // Initialize the message
        grpcdemo::Vector request;

        // Fill in the message
        request.set_data_type(grpcdemo::DataType::DOUBLE);
        request.set_vector_size(vector.size());
        request.set_vector_as_chunk(
            serialize_vector(vector, processed_idx, chunk_end_idx));

        // Write the message
        reader_writer->Write(request);

        // Update the processed idx
        processed_idx += chunk_end_idx;
    }
}

void ansys::grpc::client::GRPCClient::send_matrix(
    std::unique_ptr<::grpc::ClientReaderWriter<
        grpcdemo::Matrix, grpcdemo::Matrix>>& reader_writer,
    const std::vector<std::vector<double>>& matrix,
    const std::vector<int>& chunks) {
    // Loop over the needed chunks --> This will define how many Matrix messages
    // are needed for casting the entire Matrix message
    int processed_rows{0};
    for (int chunk_end_row : chunks) {
        // Initialize the message
        grpcdemo::Matrix request;

        // Fill in the message
        request.set_data_type(grpcdemo::DataType::DOUBLE);
        request.set_matrix_rows(matrix.size());
        request.set_matrix_cols(matrix.begin()->size());
        request.set_matrix_as_chunk(
            serialize_matrix(matrix, processed_rows, chunk_end_row));

        // Write the message
        reader_writer->Write(request);

        // Update the processed rows
        processed_rows += chunk_end_row;
    }
}

std::vector<double> ansys::grpc::client::GRPCClient::receive_vector(
    std::unique_ptr<::grpc::ClientReaderWriter<
        grpcdemo::Vector, grpcdemo::Vector>>& reader_writer,
    ::grpc::ClientContext* context) {
    // Get the metadata
    auto md = context->GetServerInitialMetadata();

    // Determine how many Vector messages we are expecting
    auto expected_messages = std::atoi(md.find("vec1-messages")->second.data());

    // Once the client has received the metadata, let us process it
    grpcdemo::Vector reply;

    if (expected_messages == 1) {
        // Read the single message
        reader_writer->Read(&reply);

        // Deserialize it!
        return deserialize_vector(reply.vector_as_chunk(), reply.vector_size(),
                                  reply.data_type());
    } else if (expected_messages > 1) {
        // Multiple messages to be processed -- Get the vector elements per
        // message / except for the last message, this has to be read from the
        // message information: vector_size
        std::vector<int> vector_sizes{};
        for (int i = 1; i < expected_messages; i++) {
            vector_sizes.push_back(MAX_ELEMS_LENGTH);
        }

        // Initialize certain variables
        std::vector<double> glued_vector{};

        // Read all incoming messages to define the full Matrix message
        for (int msg = 0; msg < expected_messages; msg++) {
            // Read the reply
            reader_writer->Read(&reply);

            if (msg == 0) {
                // First time we are reading the vectors... Load the elems to be
                // read in the final message!
                vector_sizes.push_back(reply.vector_size() -
                                       (expected_messages - 1) *
                                           MAX_ELEMS_LENGTH);
            }

            // Deserialize the incoming vector chunk
            auto aux_vector =
                deserialize_vector(reply.vector_as_chunk(),
                                   vector_sizes.at(msg), reply.data_type());

            // Append the aux_vector to the glued_vector
            glued_vector.insert(glued_vector.end(), aux_vector.begin(),
                                aux_vector.end());
        }

        // Finally return the glued vector
        return glued_vector;
    } else {
        // Return empty vector
        return std::vector<double>{};
    }
}

std::vector<std::vector<double>>
ansys::grpc::client::GRPCClient::receive_matrix(
    std::unique_ptr<::grpc::ClientReaderWriter<
        grpcdemo::Matrix, grpcdemo::Matrix>>& reader_writer,
    ::grpc::ClientContext* context) {
    // Get the metadata
    auto md = context->GetServerInitialMetadata();

    // Determine how many Vector messages we are expecting
    auto expected_messages = std::atoi(md.find("mat1-messages")->second.data());

    // Once the client has received the metadata, let us process it
    grpcdemo::Matrix reply;

    if (expected_messages == 1) {
        // Read the single message
        reader_writer->Read(&reply);

        // Deserialize it!
        return deserialize_matrix(reply.matrix_as_chunk(), reply.matrix_rows(),
                                  reply.matrix_cols(), reply.data_type());
    } else if (expected_messages > 1) {
        // Initialize certain variables
        std::vector<std::vector<double>> glued_matrix{};

        // Multiple messages to be processed -- Get the matrix rows per
        // message / except for the last message, this has to be read from
        // the message information: matrix_rows
        std::vector<int> matrix_sizes{};

        // Read all incoming messages to define the full Matrix message
        for (int msg = 0; msg < expected_messages; msg++) {
            // Read the reply
            reader_writer->Read(&reply);

            if (msg == 0) {
                // First time we are reading the matrices... Load the elems to
                // be read in the message!
                int max_rows_per_message =
                    MAX_ELEMS_LENGTH / reply.matrix_cols();

                for (int i = 1; i < expected_messages; i++) {
                    matrix_sizes.push_back(max_rows_per_message);
                }

                matrix_sizes.push_back(reply.matrix_rows() -
                                       (expected_messages - 1) *
                                           max_rows_per_message);
            }

            // Deserialize the incoming matrix chunk
            auto aux_matrix = deserialize_matrix(
                reply.matrix_as_chunk(), matrix_sizes.at(msg),
                reply.matrix_cols(), reply.data_type());

            // Append the aux_matrix to the glued_vector
            glued_matrix.insert(glued_matrix.end(), aux_matrix.begin(),
                                aux_matrix.end());
        }

        // Finally return the glued matrix
        return glued_matrix;
    } else {
        // Return empty matrix
        return std::vector<std::vector<double>>{};
    }
}

// ============================================================================
// ansys::grpc::client NAMESPACE METHODS
// ============================================================================
