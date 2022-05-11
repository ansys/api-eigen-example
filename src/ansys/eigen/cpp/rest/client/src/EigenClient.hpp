#include <restclient-cpp/connection.h>
#include <restclient-cpp/restclient.h>

#include <iostream>
#include <string>

#ifndef SRC_ANSYS_EIGEN_CPP_REST_CLIENT_SRC_EIGENCLIENT_HPP
#define SRC_ANSYS_EIGEN_CPP_REST_CLIENT_SRC_EIGENCLIENT_HPP

/**
 * @brief Namespace including the API Eigen Example Client implemented in C++.
 */
namespace ansys::rest::client {

/**
 * @brief Class containing the basic functionalities to interact with the API
 * Eigen Example server.
 *
 */
class EigenClient {
   public:
    /**
     * @brief Construct a new Eigen Client object.
     *
     * @param baseUrl - the API Eigen Example server endpoint (e.g.
     * http://127.0.0.1:18081).
     * @param user - (optional) the user in case of BasicAuthentication
     * mechanism required. Default: empty.
     * @param pwd- (optional) the password in case of BasicAuthentication
     * mechanism required. Default: empty.
     * @param timeout - (optional) the timeout to be set for aborting
     * connection. Default: 10.
     */
    EigenClient(const std::string& baseUrl,
                const std::string& user = std::string{},
                const std::string& pwd = std::string{}, int timeout = 10);

    /**
     * @brief Destroy the Eigen Client object.
     */
    ~EigenClient();

    /**
     * @brief Method to request a greeting from the endpoint server.
     */
    void request_greeting();

   private:
    /**
     * @brief The connection pointer to the endpoint server.
     */
    RestClient::Connection* _conn{nullptr};
};

/**
 * @brief Method for printing out Response objects in a common format.
 *
 * @param response - the RestClient::Response object.
 */
void print_response(const RestClient::Response& response);

}  // namespace ansys::rest::client

#endif /* SRC_ANSYS_EIGEN_CPP_REST_CLIENT_SRC_EIGENCLIENT_HPP */
