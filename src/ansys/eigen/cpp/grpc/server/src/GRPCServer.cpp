#include "GRPCServer.hpp"

#include <iostream>

// ============================================================================
// GRPCServer PUBLIC METHODS
// ============================================================================

// GRPCServer Ctor. & Dtor.
// ----------------------------------------------------------------------------

ansys::grpc::server::GRPCServer::GRPCServer() {
    // Start creating the GRPCServer object
    std::cout << "GRPCServer object created." << std::endl;
}

ansys::grpc::server::GRPCServer::~GRPCServer() {
    // Start destroying the GRPCServer object
    std::cout << "GRPCServer object destroyed." << std::endl;
}

// GRPCServer Functionalities
// ----------------------------------------------------------------------------

// ============================================================================
// GRPCServer PRIVATE METHODS
// ============================================================================

// ============================================================================
// ansys::grpc::server NAMESPACE METHODS
// ============================================================================
