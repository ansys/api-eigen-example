#include <grpcpp/grpcpp.h>

#include <Eigen/Core>

#include "generated/grpcdemo.grpc.pb.h"

#ifndef SRC_ANSYS_EIGEN_CPP_GRPC_SERVER_SRC_GRPCSERVICE_HPP
#define SRC_ANSYS_EIGEN_CPP_GRPC_SERVER_SRC_GRPCSERVICE_HPP

namespace ansys {
namespace grpc {

/**
 * @brief Namespace including the API Eigen Example Server logic (i.e. service)
 * implemented in C++.
 */
namespace service {

/**
 * @brief Class containing the server logic (i.e. service).
 */
class GRPCService final : public grpcdemo::GRPCDemo::Service {
   public:
    /**
     * @brief Construct a new GRPCDemo Service object.
     *
     * @param debug_log whether to show the enhanced debugging logs or not.
     */
    GRPCService(const bool debug_log);

    /**
     * @brief Destroy the GRPCDemo Service object.
     */
    ~GRPCService();

    /**
     * @brief Method to provide a simple greeting to the client.
     *
     * @param context the gRPC Server context.
     * @param request the gRPC request.
     * @param response the gRPC response this method will fill.
     * @return ::grpc::Status
     */
    ::grpc::Status SayHello(::grpc::ServerContext* context,
                            const ::grpcdemo::HelloRequest* request,
                            ::grpcdemo::HelloReply* response) override;

    /**
     * @brief Method to provide a flipped vector to the client.
     *
     * @param context the gRPC Server context.
     * @param stream the gRPC stream.
     * @return ::grpc::Status
     */
    ::grpc::Status FlipVector(
        ::grpc::ServerContext* context,
        ::grpc::ServerReaderWriter<::grpcdemo::Vector, ::grpcdemo::Vector>*
            stream) override;

    /**
     * @brief Method to provide the addition of Vector messages.
     *
     * @param context the gRPC Server context.
     * @param stream the gRPC stream.
     * @return ::grpc::Status
     */
    ::grpc::Status AddVectors(
        ::grpc::ServerContext* context,
        ::grpc::ServerReaderWriter<::grpcdemo::Vector, ::grpcdemo::Vector>*
            stream) override;

    /**
     * @brief Method to provide the dot product of Vector messages.
     *
     * @param context the gRPC Server context.
     * @param stream the gRPC stream.
     * @return ::grpc::Status
     */
    ::grpc::Status MultiplyVectors(
        ::grpc::ServerContext* context,
        ::grpc::ServerReaderWriter<::grpcdemo::Vector, ::grpcdemo::Vector>*
            stream) override;

    /**
     * @brief Method to provide the addition of Matrix messages.
     *
     * @param context the gRPC Server context.
     * @param stream the gRPC stream.
     * @return ::grpc::Status
     */
    ::grpc::Status AddMatrices(
        ::grpc::ServerContext* context,
        ::grpc::ServerReaderWriter<::grpcdemo::Matrix, ::grpcdemo::Matrix>*
            stream) override;

    /**
     * @brief Method to provide the multiplication of Matrix messages.
     *
     * @param context the gRPC Server context.
     * @param stream the gRPC stream.
     * @return ::grpc::Status
     */
    ::grpc::Status MultiplyMatrices(
        ::grpc::ServerContext* context,
        ::grpc::ServerReaderWriter<::grpcdemo::Matrix, ::grpcdemo::Matrix>*
            stream) override;

   private:
    /**
     * @brief Boolean indicating whether to show the debugging logs or not
     */
    bool _debug_log;

    /**
     * @brief Method used to deserialize a Vector message into an
     * Eigen::VectorXd object.
     *
     * @param bytes the chunk of bytes from where the vector is deserialized.
     * @param length the length of the vector we are deserializing.
     * @param type the type of data inside the vector (e.g. double, int...).
     * @return Eigen::VectorXd
     */
    Eigen::VectorXd deserialize_vector(const std::string& bytes,
                                       const int length,
                                       grpcdemo::DataType type);
    /**
     * @brief Method used to serialize an Eigen::VectorXd object into a Vector
     * message.
     *
     * @param vector the Eigen::VectorXd to be serialized.
     * @param start the starting index to serialize.
     * @param end the last index to serialize (not included).
     * @return std::string
     */
    std::string serialize_vector(const Eigen::VectorXd& vector, const int start,
                                 const int end);

    /**
     * @brief Method used to deserialize a Matrix message into an
     * Eigen::MatrixXd object.
     *
     * @param bytes the chunk of bytes from where the matrix is deserialized.
     * @param rows the number of rows of the matrix we are deserializing.
     * @param cols the number of columns of the matrix we are deserializing.
     * @param type the type of data inside the matrix (e.g. double, int...).
     * @return Eigen::MatrixXd
     */
    Eigen::MatrixXd deserialize_matrix(const std::string& bytes, const int rows,
                                       const int cols, grpcdemo::DataType type);

    /**
     * @brief Method used to serialize an Eigen::MatrixXd object into a Matrix
     * message.
     *
     * @param matrix the Eigen::MatrixXd to be serialized.
     * @param start the starting index to serialize.
     * @param end the last index to serialize (not included).
     * @return std::string
     */
    std::string serialize_matrix(const Eigen::MatrixXd& matrix, const int start,
                                 const int end);

    /**
     * @brief Method in charge of providing a set of Eigen::VectorXd objects
     * from a stream of Vector messages.
     *
     * @param reader_writer the gRPC reader-writer in the bidirectional stream
     * protocol.
     * @param context the gRPC context.
     * @return std::vector<Eigen::VectorXd>
     */
    std::vector<Eigen::VectorXd> receive_vectors(
        ::grpc::ServerReaderWriter<grpcdemo::Vector, grpcdemo::Vector>*
            reader_writer,
        ::grpc::ServerContext* context);

    /**
     * @brief Method in charge of providing a set of Eigen::MatrixXd objects
     * from a stream of Matrix messages.
     *
     * @param reader_writer the gRPC reader-writer in the bidirectional stream
     * protocol.
     * @param context the gRPC context.
     * @return std::vector<Eigen::MatrixXd>
     */
    std::vector<Eigen::MatrixXd> receive_matrices(
        ::grpc::ServerReaderWriter<grpcdemo::Matrix, grpcdemo::Matrix>*
            reader_writer,
        ::grpc::ServerContext* context);

    /**
     * @brief Method in charge of sending the resulting vector of the operation
     * through the protocol.
     *
     * @param reader_writer the gRPC reader-writer in the bidirectional stream
     * protocol.
     * @param context the gRPC context.
     * @param vector the vector to be sent.
     */
    void send_vector(
        ::grpc::ServerReaderWriter<grpcdemo::Vector, grpcdemo::Vector>*
            reader_writer,
        ::grpc::ServerContext* context, const Eigen::VectorXd& vector);

    /**
     * @brief Method in charge of sending the resulting matrix of the operation
     * through the protocol.
     *
     * @param reader_writer the gRPC reader-writer in the bidirectional stream
     * protocol.
     * @param context the gRPC context.
     * @param matrix the matrix to be sent.
     */
    void send_matrix(
        ::grpc::ServerReaderWriter<grpcdemo::Matrix, grpcdemo::Matrix>*
            reader_writer,
        ::grpc::ServerContext* context, const Eigen::MatrixXd& matrix);
};

}  // namespace service
}  // namespace grpc
}  // namespace ansys

#endif /* SRC_ANSYS_EIGEN_CPP_GRPC_SERVER_SRC_GRPCSERVICE_HPP */
