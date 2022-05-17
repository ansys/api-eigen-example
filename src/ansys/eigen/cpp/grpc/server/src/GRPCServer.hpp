#ifndef SRC_ANSYS_EIGEN_CPP_GRPC_SERVER_SRC_GRPCSERVER_HPP
#define SRC_ANSYS_EIGEN_CPP_GRPC_SERVER_SRC_GRPCSERVER_HPP

namespace ansys {
namespace grpc {

/**
 * @brief Namespace including the API Eigen Example Server implemented in C++.
 */
namespace server {

/**
 * @brief Class containing the server logic.
 */
class GRPCServer {
   public:
    /**
     * @brief Construct a new GRPC Server object.
     */
    GRPCServer();

    /**
     * @brief Destroy the GRPC Server object.
     */
    ~GRPCServer();

   private:
};

}  // namespace client
}  // namespace grpc
}  // namespace ansys

#endif /* SRC_ANSYS_EIGEN_CPP_GRPC_SERVER_SRC_GRPCSERVER_HPP */
