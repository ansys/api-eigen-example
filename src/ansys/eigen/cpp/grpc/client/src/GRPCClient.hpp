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
     */
    GRPCClient(const std::string host = std::string{"0.0.0.0"},
               const int port = 50000);

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
     * @param vector the  std::vector<double> to be serialized.
     * @return std::string
     */
    std::string serialize_vector(const std::vector<double>& vector);

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
     * @return std::string
     */
    std::string serialize_matrix(
        const std::vector<std::vector<double>>& matrix);
};

}  // namespace client
}  // namespace grpc
}  // namespace ansys

#endif /* SRC_ANSYS_EIGEN_CPP_GRPC_CLIENT_SRC_GRPCCLIENT_HPP */
