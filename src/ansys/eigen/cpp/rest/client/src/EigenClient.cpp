#include "EigenClient.hpp"

#include <stdio.h>
#include <stdlib.h>

// ============================================================================
// EigenClient PUBLIC METHODS
// ============================================================================

// EigenClient Ctor. & Dtor.
// ----------------------------------------------------------------------------

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

// EigenClient Functionalities
// ----------------------------------------------------------------------------

void ansys::rest::client::EigenClient::request_greeting() {
    // Perform the greeting request.
    auto response = _conn->get("/");

    // Print out the server's response
    print_response(response);
}

std::vector<double> ansys::rest::client::EigenClient::add_vectors(
    const std::vector<double>& vec1, const std::vector<double>& vec2) {
    // Start by posting the Vectors
    auto id1 = post_vector(vec1);
    auto id2 = post_vector(vec2);

    // Once the vectors are posted, request the operation
    std::string request{"/add/Vectors/" + std::to_string(id1) + "/" +
                        std::to_string(id2)};
    fprintf(stdout, "Request: GET %s\n", request.c_str());
    auto result = _conn->get(request);

    // Let us read the result from the returned JSON
    Json::Value aux_value;
    std::string err{};
    bool success{true};

    // Let us declare our JSON Reader
    Json::CharReaderBuilder builder;
    const std::unique_ptr<Json::CharReader> reader(builder.newCharReader());

    success = reader->parse(
        result.body.c_str(),
        result.body.c_str() + static_cast<int>(result.body.length()),
        &aux_value, &err);

    print_response(result);
    if (!success) {
        fprintf(stderr, "Failure parsing server response.\n");
        return std::vector<double>{};
    } else {
        return json_to_vector(aux_value["vector-addition"]["result"]);
    }
}

double ansys::rest::client::EigenClient::multiply_vectors(
    const std::vector<double>& vec1, const std::vector<double>& vec2) {
    // Start by posting the Vectors
    auto id1 = post_vector(vec1);
    auto id2 = post_vector(vec2);

    // Once the vectors are posted, request the operation
    std::string request{"/multiply/Vectors/" + std::to_string(id1) + "/" +
                        std::to_string(id2)};
    fprintf(stdout, "Request: GET %s\n", request.c_str());
    auto result = _conn->get(request);

    // Let us read the result from the returned JSON
    Json::Value aux_value;
    std::string err{};
    bool success{true};

    // Let us declare our JSON Reader
    Json::CharReaderBuilder builder;
    const std::unique_ptr<Json::CharReader> reader(builder.newCharReader());

    success = reader->parse(
        result.body.c_str(),
        result.body.c_str() + static_cast<int>(result.body.length()),
        &aux_value, &err);

    print_response(result);
    if (!success) {
        fprintf(stderr, "Failure parsing server response.\n");
        return 0.0;
    } else {
        return aux_value["vector-multiplication"]["result"].asDouble();
    }
}

// ============================================================================
// EigenClient PRIVATE METHODS
// ============================================================================

int ansys::rest::client::EigenClient::post_vector(
    const std::vector<double>& input) {
    // Declare a Json::Value auxiliary buffer
    Json::Value aux_value;

    // Let us declare our JSON Reader
    Json::CharReaderBuilder builder;
    const std::unique_ptr<Json::CharReader> reader(builder.newCharReader());

    // Let us start by parsing the vector into a string...
    // .. and posting the vectors to the server
    aux_value["value"] = vector_to_json(input);

    Json::FastWriter fastWriter;
    std::string output = fastWriter.write(aux_value);
    fprintf(stdout, "Request: POST /Vectors Content: %s", output.c_str());

    auto response = _conn->post("/Vectors", output);
    aux_value.clear();

    // Let us read the ids from the returned JSON
    std::string err{};
    bool success{true};
    int id{0};

    success = reader->parse(
        response.body.c_str(),
        response.body.c_str() + static_cast<int>(response.body.length()),
        &aux_value, &err);

    print_response(response);
    if (!success) {
        fprintf(stderr, "Failure parsing server response.\n");
        return -1;
    } else {
        id = aux_value["vector"]["id"].asInt();
    }
    aux_value.clear();

    // Finally, return the ID
    return id;
}

Json::Value ansys::rest::client::EigenClient::vector_to_json(
    const std::vector<double>& input) {
    // Declare your output JSON
    Json::Value vector;

    // Iterate over your vector and append values to the output JSON
    for (const auto& elem : input) {
        vector.append(elem);
    }

    // Return the JSON
    return vector;
}

std::vector<double> ansys::rest::client::EigenClient::json_to_vector(
    const Json::Value& input) {
    // Declare your output std::vector
    std::vector<double> vector{};

    // Iterate over your JSON and append values to the output vector
    for (const auto& elem : input) {
        vector.push_back(elem.asDouble());
    }

    // Return the std::vector
    return vector;
}

// ============================================================================
// ansys::rest::client NAMESPACE METHODS
// ============================================================================

void ansys::rest::client::print_response(const RestClient::Response& response) {
    fprintf(stdout, "Response: Code - %d; Body: %s\n", response.code,
            response.body.c_str());
}