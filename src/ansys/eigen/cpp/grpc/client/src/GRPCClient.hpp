#include <grpcpp/grpcpp.h>

#include <memory>
#include <string>
#include <vector>

#include "generated/grpcdemo.grpc.pb.h"

#ifndef SRC_ANSYS_EIGEN_CPP_GRPC_CLIENT_SRC_GRPCCLIENT_HPP
#define SRC_ANSYS_EIGEN_CPP_GRPC_CLIENT_SRC_GRPCCLIENT_HPP

namespace ansys {
namespace grpc {

/**
 * @brief Namespace including the API Eigen Example Client implemented in C++.
 */
namespace client {

/**
 * @brief Class containing the basic functionalities to interact with the API
 * Eigen Example server.
 *
 */
class GRPCClient {
   public:
    /**
     * @brief Construct a new GRPC Client object.
     *
     * @param host the host (DNS/IP) where the server is located.
     * Default: 0.0.0.0.
     * @param port the port through which the server is exposed. Default:
     * 50000.
     * @param debug_log whether to show the enhanced debugging logs or not.
     * Default: false.
     */
    GRPCClient(const std::string host = std::string{"0.0.0.0"},
               const int port = 50000, const bool debug_log = false);

    /**
     * @brief Destroy the GRPC Client object.
     */
    ~GRPCClient();

    /**
     * @brief Method to request a greeting from the endpoint server.
     *
     * @param name the name of the entity requesting the greeting (i.e. us).
     */
    void request_greeting(const std::string& name);

    /**
     * @brief Method in charge of requesting a vector position flip to the
     * endpoint server.
     *
     * @param vec the first vector involved in the operation.
     * @return std::vector<double>
     */
    std::vector<double> flip_vector(const std::vector<double>& vec);

    /**
     * @brief Method in charge of requesting a vector addition to the endpoint
     * server.
     *
     * @param vec1 the first vector involved in the operation.
     * @param vec2 the second vector involved in the operation.
     * @return std::vector<double>
     */
    std::vector<double> add_vectors(const std::vector<double>& vec1,
                                    const std::vector<double>& vec2);

    /**
     * @brief Method in charge of requesting a vector dot product to the
     * endpoint server.
     *
     * @param vec1 the first vector involved in the operation.
     * @param vec2 the second vector involved in the operation.
     * @return double
     */
    double multiply_vectors(const std::vector<double>& vec1,
                            const std::vector<double>& vec2);

    /**
     * @brief Method in charge of requesting a matrix addition to the
     * endpoint server.
     *
     * @param mat1 the first matrix involved in the operation.
     * @param mat2 the second matrix involved in the operation.
     * @return std::vector<std::vector<double>>
     */
    std::vector<std::vector<double>> add_matrices(
        const std::vector<std::vector<double>>& mat1,
        const std::vector<std::vector<double>>& mat2);

    /**
     * @brief Method in charge of requesting a matrix multiplication to the
     * endpoint server.
     *
     * @param mat1 the first matrix involved in the operation.
     * @param mat2 the second matrix involved in the operation.
     * @return std::vector<std::vector<double>>
     */
    std::vector<std::vector<double>> multiply_matrices(
        const std::vector<std::vector<double>>& mat1,
        const std::vector<std::vector<double>>& mat2);

   private:
    /**
     * @brief A unique pointer to the stub which defines the gRPC connection
     * (Channel).
     */
    std::unique_ptr<grpcdemo::GRPCDemo::Stub> _stub;

    /**
     * @brief Boolean indicating whether to show the debugging logs or not
     */
    bool _debug_log;

    /**
     * @brief Method in charge of defining the Client Metadata in the
     * bidirectional stream transfer of Vector messages.
     *
     * @param context the gRPC context.
     * @param vec1 the vector to be transmitted.
     * @param vec2 (optional) the second vector to be transmitted.
     * @return std::vector<std::vector<int>>
     */
    std::vector<std::vector<int>> define_vecstream_metadata(
        ::grpc::ClientContext* context, const std::vector<double>& vec1,
        const std::vector<double>& vec2 = {});

    /**
     * @brief Set the Vector-specific message metadata (i.e. how many partial
     * Vector messages constitute an entire Vector).
     *
     * @param context the gRPC context.
     * @param vec the vector to be transmitted.
     * @param vec_name the identifier of the vector.
     * @return std::vector<int>
     */
    std::vector<int> set_vector_metadata(::grpc::ClientContext* context,
                                         const std::vector<double>& vec,
                                         const std::string& vec_name);

    /**
     * @brief Method in charge of defining the Client Metadata in the
     * bidirectional stream transfer of Matrix messages.
     *
     * @param context the gRPC context.
     * @param mat1 the first matrix to be transmitted.
     * @param mat2 the second matrix to be transmitted.
     * @return std::vector<std::vector<int>>
     */
    std::vector<std::vector<int>> define_matstream_metadata(
        ::grpc::ClientContext* context,
        const std::vector<std::vector<double>>& mat1,
        const std::vector<std::vector<double>>& mat2);

    /**
     * @brief Set the Matrix-specific message metadata (i.e. how many partial
     * Matrix messages constitute an entire Matrix).
     *
     * @param context the gRPC context.
     * @param mat the matrix to be transmitted.
     * @param mat_name the identifier of the matrix.
     * @return std::vector<int>
     */
    std::vector<int> set_matrix_metadata(
        ::grpc::ClientContext* context,
        const std::vector<std::vector<double>>& mat,
        const std::string& mat_name);

    /**
     * @brief Method used to deserialize a Vector message into an
     *  std::vector<double> object.
     *
     * @param bytes the chunk of bytes from where the vector is deserialized.
     * @param length the length of the vector we are deserializing.
     * @param type the type of data inside the vector (e.g. double, int...).
     * @return  std::vector<double>
     */
    std::vector<double> deserialize_vector(const std::string& bytes,
                                           const int length,
                                           grpcdemo::DataType type);
    /**
     * @brief Method used to serialize an  std::vector<double> object into a
     * Vector message.
     *
     * @param vector the std::vector<double> to be serialized.
     * @param start the starting index to serialize.
     * @param end the last index to serialize (not included).
     * @return std::string
     */
    std::string serialize_vector(const std::vector<double>& vector,
                                 const int start, const int end);

    /**
     * @brief Method used to deserialize a Matrix message into an
     * std::vector<std::vector<double>> object.
     *
     * @param bytes the chunk of bytes from where the matrix is deserialized.
     * @param rows the number of rows of the matrix we are deserializing.
     * @param cols the number of columns of the matrix we are deserializing.
     * @param type the type of data inside the matrix (e.g. double, int...).
     * @return std::vector<std::vector<double>>
     */
    std::vector<std::vector<double>> deserialize_matrix(
        const std::string& bytes, const int rows, const int cols,
        grpcdemo::DataType type);

    /**
     * @brief Method used to serialize an std::vector<std::vector<double>>
     * object into a Matrix message.
     *
     * @param matrix the std::vector<std::vector<double>> to be serialized.
     * @param start the starting row index to serialize.
     * @param end the last row index to serialize (not included).
     * @return std::string
     */
    std::string serialize_matrix(const std::vector<std::vector<double>>& matrix,
                                 const int start, const int end);

    /**
     * @brief Method in charge of sending a message for stream-based inputs in
     * RPC method. Targeted to Vector messages.
     *
     * @param reader_writer the writer used for streaming the messages.
     * @param vector the message to be streamed.
     * @param chunks number of elements in each individual Vector message.
     */
    void send_vector(std::unique_ptr<::grpc::ClientReaderWriter<
                         grpcdemo::Vector, grpcdemo::Vector>>& reader_writer,
                     const std::vector<double>& vector,
                     const std::vector<int>& chunks);

    /**
     * @brief  Method in charge of sending a message for stream-based inputs in
     * RPC method. Targeted to Matrix messages.
     *
     * @param reader_writer the writer used for streaming the messages.
     * @param matrix the message to be streamed.
     * @param chunks number of elements in each individual Vector message.
     */
    void send_matrix(std::unique_ptr<::grpc::ClientReaderWriter<
                         grpcdemo::Matrix, grpcdemo::Matrix>>& reader_writer,
                     const std::vector<std::vector<double>>& matrix,
                     const std::vector<int>& chunks);

    /**
     * @brief Method in charge of providing the resulting Vector of an operation
     * requested to the server from a stream of partial Vector messages.
     *
     * @param reader_writer the gRPC reader-writer in the bidirectional stream
     * protocol.
     * @param context the gRPC context.
     * @return std::vector<double>
     */
    std::vector<double> receive_vector(
        std::unique_ptr<::grpc::ClientReaderWriter<
            grpcdemo::Vector, grpcdemo::Vector>>& reader_writer,
        ::grpc::ClientContext* context);

    /**
     * @brief Method in charge of providing the resulting Matrix of an operation
     * requested to the server from a stream of partial Matrix messages.
     *
     * @param reader_writer the gRPC reader-writer in the bidirectional stream
     * protocol.
     * @param context the gRPC context.
     * @return std::vector<std::vector<double>>
     */
    std::vector<std::vector<double>> receive_matrix(
        std::unique_ptr<::grpc::ClientReaderWriter<
            grpcdemo::Matrix, grpcdemo::Matrix>>& reader_writer,
        ::grpc::ClientContext* context);
};

}  // namespace client
}  // namespace grpc
}  // namespace ansys

#endif /* SRC_ANSYS_EIGEN_CPP_GRPC_CLIENT_SRC_GRPCCLIENT_HPP */
