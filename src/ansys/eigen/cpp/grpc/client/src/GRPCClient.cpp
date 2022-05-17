#include "GRPCClient.hpp"

#include <iostream>

// ============================================================================
// GRPCClient PUBLIC METHODS
// ============================================================================

// GRPCClient Ctor. & Dtor.
// ----------------------------------------------------------------------------

ansys::grpc::client::GRPCClient::GRPCClient() {
    // Start creating the GRPCClient object
    std::cout << "GRPCClient object created." << std::endl;
}

ansys::grpc::client::GRPCClient::~GRPCClient() {
    // Start destroying the GRPCClient object
    std::cout << "GRPCClient object destroyed." << std::endl;
}

// GRPCClient Functionalities
// ----------------------------------------------------------------------------

// ============================================================================
// GRPCClient PRIVATE METHODS
// ============================================================================

// ============================================================================
// ansys::grpc::client NAMESPACE METHODS
// ============================================================================
