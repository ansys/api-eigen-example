#include <jsoncpp/json/json.h>
#include <restclient-cpp/connection.h>
#include <restclient-cpp/restclient.h>

#include <iostream>
#include <memory>
#include <string>
#include <vector>

#ifndef SRC_ANSYS_EIGEN_CPP_REST_CLIENT_SRC_EIGENCLIENT_HPP
#define SRC_ANSYS_EIGEN_CPP_REST_CLIENT_SRC_EIGENCLIENT_HPP

namespace ansys {
namespace rest {

/**
 * @brief Namespace including the API Eigen Example Client implemented in C++.
 */
namespace client {

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
     * @param baseUrl the API Eigen Example server endpoint (e.g.
     * http://127.0.0.1:18080).
     * @param user (optional) the user in case of BasicAuthentication mechanism
     * required. Default: empty.
     * @param pwd (optional) the password in case of BasicAuthentication
     * mechanism required. Default: empty.
     * @param timeout (optional) the timeout to be set for aborting connection.
     * Default: 10.
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

    /**
     * @brief Method in charge of requesting a vector addition to the endpoint
     * server.
     *
     * @param vec1 the first vector involved in the operation.
     * @param vec2 the second vector involved in the operation.
     * @return std::vector<double>
     */
    std::vector<double> add_vectors(const std::vector<double>& vec1,
                                    const std::vector<double>& vec2);

    /**
     * @brief Method in charge of requesting a vector dot product to the
     * endpoint server.
     *
     * @param vec1 the first vector involved in the operation.
     * @param vec2 the second vector involved in the operation.
     * @return double
     */
    double multiply_vectors(const std::vector<double>& vec1,
                            const std::vector<double>& vec2);

    /**
     * @brief Method in charge of requesting a matrix addition to the
     * endpoint server.
     *
     * @param mat1 the first matrix involved in the operation.
     * @param mat2 the second matrix involved in the operation.
     * @return std::vector<std::vector<double>>
     */
    std::vector<std::vector<double>> add_matrices(
        const std::vector<std::vector<double>>& mat1,
        const std::vector<std::vector<double>>& mat2);

    /**
     * @brief Method in charge of requesting a matrix multiplication to the
     * endpoint server.
     *
     * @param mat1 the first matrix involved in the operation.
     * @param mat2 the second matrix involved in the operation.
     * @return std::vector<std::vector<double>>
     */
    std::vector<std::vector<double>> multiply_matrices(
        const std::vector<std::vector<double>>& mat1,
        const std::vector<std::vector<double>>& mat2);

   private:
    /**
     * @brief The connection pointer to the endpoint server.
     */
    RestClient::Connection* _conn{nullptr};

    /**
     * @brief Method in charge of connecting to the endpoint server to POST a
     * Vector Resource.
     *
     * @param input the vector we are interested in posting.
     * @return int - the ID of the posted vector.
     */
    int post_vector(const std::vector<double>& input);

    /**
     * @brief Method in charge of connecting to the endpoint server to POST a
     * Matrix Resource.
     *
     * @param input the matrix we are interested in posting.
     * @return int - the ID of the posted matrix.
     */
    int post_matrix(const std::vector<std::vector<double>>& input);

    /**
     * @brief Method in charge of transforming a std::vector of type double to a
     * JSON object.
     *
     * @param input the vector to be formatted as a JSON object.
     * @return Json::Value
     */
    Json::Value vector_to_json(const std::vector<double>& input);

    /**
     * @brief Method in charge of transforming a std::vector<std::vecto> of type
     * double to a JSON object.
     *
     * @param input the matrix to be formatted as a JSON object.
     * @return Json::Value
     */
    Json::Value matrix_to_json(const std::vector<std::vector<double>>& input);

    /**
     * @brief Method in charge of transforming a JSON object which represents a
     * vector into a std::vector<double>.
     *
     * @param input the JSON object to be formatted as a vector.
     * @return std::vector<double>
     */
    std::vector<double> json_to_vector(const Json::Value& input);

    /**
     * @brief Method in charge of transforming a JSON object which represents a
     * matrix into a std::vector<std::vector<double>>.
     *
     * @param input the JSON object to be formatted as a matrix.
     * @return std::vector<std::vector<double>>
     */
    std::vector<std::vector<double>> json_to_matrix(const Json::Value& input);
};

/**
 * @brief Method for printing out Response objects in a common format.
 *
 * @param response the RestClient::Response object.
 */
void print_response(const RestClient::Response& response);

}  // namespace client
}  // namespace rest
}  // namespace ansys

#endif /* SRC_ANSYS_EIGEN_CPP_REST_CLIENT_SRC_EIGENCLIENT_HPP */
