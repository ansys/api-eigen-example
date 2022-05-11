#include "EigenClient.hpp"

#include <stdio.h>
#include <stdlib.h>

ansys::rest::client::EigenClient::EigenClient(const std::string& baseUrl,
                                              const std::string& user,
                                              const std::string& pwd,
                                              int timeout) {
    // Start creating the EigenClient object
    fprintf(stdout, "EigenClient object created.\n");

    // Initialize the RestClient
    RestClient::init();

    // Get a connection object
    _conn = new RestClient::Connection(baseUrl);

    // Add the BasicAuth headers if user and pwd available
    if (!user.empty() && !pwd.empty()) {
        fprintf(stdout, "Setting BasicAuthentication credentials.\n");
        _conn->SetBasicAuth(user, pwd);
    }

    // Set connection timeout
    _conn->SetTimeout(timeout);

    // Add required headers for interacting with the API Eigen Example server
    RestClient::HeaderFields headers;
    headers["Accept"] = "application/json";
    headers["Content-Type"] = "application/json";
    _conn->SetHeaders(headers);
}

ansys::rest::client::EigenClient::~EigenClient() {
    // Start destroying the EigenClient object
    fprintf(stdout, "EigenClient object destroyed.\n");

    // Delete the client connection
    delete _conn;
    _conn = nullptr;

    // Disable the client
    RestClient::disable();
}

void ansys::rest::client::EigenClient::request_greeting() {
    // Perform the greeting request.
    auto response = _conn->get("/");

    // Print out the server's response
    print_response(response);
}

void ansys::rest::client::print_response(const RestClient::Response& response) {
    fprintf(stdout, "Response: Code - %d; Body: %s\n", response.code, response.body.c_str());
}