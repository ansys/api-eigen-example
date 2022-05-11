#include <jsoncpp/json/json.h>
#include <restclient-cpp/connection.h>
#include <restclient-cpp/restclient.h>

#include <iostream>
#include <memory>
#include <string>
#include <vector>

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

    std::vector<double> add_vectors(const std::vector<double>& vec1,
                                    const std::vector<double>& vec2);

    double multiply_vectors(const std::vector<double>& vec1,
                            const std::vector<double>& vec2);

    std::vector<std::vector<double>> add_matrices(
        const std::vector<std::vector<double>>& mat1,
        const std::vector<std::vector<double>>& mat2);

    std::vector<std::vector<double>> multiply_matrices(
        const std::vector<std::vector<double>>& mat1,
        const std::vector<std::vector<double>>& mat2);

   private:
    /**
     * @brief The connection pointer to the endpoint server.
     */
    RestClient::Connection* _conn{nullptr};

    RestClient::Response get(const std::string& url, const std::string& data);

    int post_vector(const std::vector<double>& input);

    Json::Value vector_to_json(const std::vector<double>& input);

    std::vector<double> json_to_vector(const Json::Value& input);

    std::vector<std::vector<double>> json_to_matrix(const Json::Value& input);
};

/**
 * @brief Method for printing out Response objects in a common format.
 *
 * @param response - the RestClient::Response object.
 */
void print_response(const RestClient::Response& response);

}  // namespace ansys::rest::client

#endif /* SRC_ANSYS_EIGEN_CPP_REST_CLIENT_SRC_EIGENCLIENT_HPP */
