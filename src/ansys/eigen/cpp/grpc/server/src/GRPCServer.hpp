#include <grpcpp/grpcpp.h>

#include <memory>
#include <string>

#ifndef SRC_ANSYS_EIGEN_CPP_GRPC_SERVER_SRC_GRPCSERVER_HPP
#define SRC_ANSYS_EIGEN_CPP_GRPC_SERVER_SRC_GRPCSERVER_HPP

namespace ansys {
namespace grpc {

/**
 * @brief Namespace including the API Eigen Example Server implemented in C++.
 */
namespace server {

/**
 * @brief Class for deploying the API Eigen Example Server via its serve()
 * method.
 */
class GRPCServer {
   public:
    /**
     * @brief Construct a new GRPCServer object.
     */
    GRPCServer();

    /**
     * @brief Destroy the GRPCServer object.
     */
    ~GRPCServer();

    /**
     * @brief Method for serving our application.
     *
     * @param host the host (DNS/IP) in which we want to server our app.
     * Default: 0.0.0.0.
     * @param port the port in which we want to server our app. Default:
     * 50000.
     */
    void serve(const std::string host = std::string{"0.0.0.0"},
               const int port = 50000);

   private:
    /**
     * @brief Pointer to the server instance. Required for shutting down when
     * cancelled.
     */
    std::unique_ptr<::grpc::Server> _server;
};

}  // namespace server
}  // namespace grpc
}  // namespace ansys

#endif /* SRC_ANSYS_EIGEN_CPP_GRPC_SERVER_SRC_GRPCSERVER_HPP */
