#include "GRPCService.hpp"

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
    ::grpcdemo::HelloReply* response) {}

::grpc::Status ansys::grpc::service::GRPCService::FlipVector(
    ::grpc::ServerContext* context, const ::grpcdemo::Vector* request,
    ::grpcdemo::Vector* response) {}

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

// ============================================================================
// ansys::grpc::server NAMESPACE METHODS
// ============================================================================
