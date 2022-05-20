#include "GRPCServer.hpp"

#include <iostream>

#include "GRPCService.hpp"

// ============================================================================
// GRPCServer PUBLIC METHODS
// ============================================================================

// GRPCServer Ctor. & Dtor.
// ----------------------------------------------------------------------------

ansys::grpc::server::GRPCServer::GRPCServer() {
    std::cout << "Instantiating our server..." << std::endl;
}

ansys::grpc::server::GRPCServer::~GRPCServer() {
    // Always shutdown the server first
    std::cout << "Shutting down our server..." << std::endl;
    _server->Shutdown();
}

// GRPCServer Functionalities
// ----------------------------------------------------------------------------

void ansys::grpc::server::GRPCServer::serve(const std::string host,
                                            const int port,
                                            const bool debug_log) {
    // Start by defining our server address
    std::string server_address = host + ":" + std::to_string(port);

    // Initialize our service
    ansys::grpc::service::GRPCService service{debug_log};

    ::grpc::ServerBuilder builder;
    // Listen on the given address without any authentication mechanism.
    builder.AddListeningPort(server_address,
                             ::grpc::InsecureServerCredentials());

    // Register "service" as the instance through which we'll communicate with
    // clients. In this case it corresponds to a *synchronous* service.
    builder.RegisterService(&service);

    // Finally assemble the server.
    _server = builder.BuildAndStart();
    std::cout << "Server listening on " << server_address << std::endl;

    // Wait for the server to shutdown. Note that some other thread must be
    // responsible for shutting down the server for this call to ever return.
    _server->Wait();
}