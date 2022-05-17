#include <grpcpp/grpcpp.h>

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
     */
    GRPCService();

    /**
     * @brief Destroy the GRPCDemo Service object.
     */
    ~GRPCService();

    ::grpc::Status SayHello(::grpc::ServerContext* context,
                            const ::grpcdemo::HelloRequest* request,
                            ::grpcdemo::HelloReply* response);

    ::grpc::Status FlipVector(::grpc::ServerContext* context,
                              const ::grpcdemo::Vector* request,
                              ::grpcdemo::Vector* response);

    ::grpc::Status AddVectors(::grpc::ServerContext* context,
                              ::grpc::ServerReader< ::grpcdemo::Vector>* reader,
                              ::grpcdemo::Vector* response);

    ::grpc::Status MultiplyVectors(
        ::grpc::ServerContext* context,
        ::grpc::ServerReader< ::grpcdemo::Vector>* reader,
        ::grpcdemo::Vector* response);

    ::grpc::Status AddMatrices(
        ::grpc::ServerContext* context,
        ::grpc::ServerReader< ::grpcdemo::Matrix>* reader,
        ::grpcdemo::Matrix* response);

    ::grpc::Status MultiplyMatrices(
        ::grpc::ServerContext* context,
        ::grpc::ServerReader< ::grpcdemo::Matrix>* reader,
        ::grpcdemo::Matrix* response);

   private:
};

}  // namespace service
}  // namespace grpc
}  // namespace ansys

#endif /* SRC_ANSYS_EIGEN_CPP_GRPC_SERVER_SRC_GRPCSERVICE_HPP */
