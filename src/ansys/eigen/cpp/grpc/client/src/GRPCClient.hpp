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
     */
    GRPCClient();

    /**
     * @brief Destroy the GRPC Client object.
     */
    ~GRPCClient();

   private:
};

}  // namespace client
}  // namespace grpc
}  // namespace ansys

#endif /* SRC_ANSYS_EIGEN_CPP_GRPC_CLIENT_SRC_GRPCCLIENT_HPP */
