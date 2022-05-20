#include <crow.h>

#include "RestDb.hpp"

#ifndef SRC_ANSYS_EIGEN_CPP_REST_SERVER_SRC_RESTSERVER_HPP
#define SRC_ANSYS_EIGEN_CPP_REST_SERVER_SRC_RESTSERVER_HPP

namespace ansys {
namespace rest {

/**
 * @brief Namespace including the API Eigen Example Server implemented in C++.
 */
namespace server {

/**
 * @brief Class containing the server logic.
 */
class RestServer {
   public:
    /**
     * @brief Construct a new Rest Server object.
     */
    RestServer();

    /**
     * @brief Destroy the Rest Server object.
     */
    ~RestServer();

    /**
     * @brief Method for serving our application.
     *
     * @param port the port in which we want to server our app. Default:
     * 18080.
     * @param async whether we want to run application asynchronously or not.
     * Default: false.
     * @param logLevel the logging level of our server. Default: Info.
     */
    void serve(const int port = 18080, const bool async = false,
               const crow::LogLevel logLevel = crow::LogLevel::Info);

    /**
     * @brief Get the app object.
     *
     * @return crow::SimpleApp&
     */
    crow::SimpleApp& get_app() { return _app; }

   private:
    /**
     * @brief The server's DB.
     */
    db::RestDb _db;

    /**
     * @brief The server CROW application.
     */
    crow::SimpleApp _app;

    /**
     * @brief Method defining the "Vectors" Resource endpoints.
     */
    void vector_resource_endpoints();

    /**
     * @brief Method defining the "Matrices" Resource endpoints.
     */
    void matrix_resource_endpoints();

    /**
     * @brief Method defining the "Vectors" operations endpoints.
     */
    void vector_operations_endpoints();

    /**
     * @brief Method defining the "Matrices" operations endpoints.
     */
    void matrix_operations_endpoints();

    /**
     * @brief Method in charge of retrieving the Vector resources from the DB
     * and adding them.
     *
     * @param id1 - the id of the first Vector.
     * @param id2 - the id of the second Vector.
     * @return crow::response
     */
    crow::response add_vectors(int id1, int id2);

    /**
     * @brief Method in charge of retrieving the Vector resources from the DB
     * and performing their dot product.
     *
     * @param id1 - the id of the first Vector.
     * @param id2 - the id of the second Vector.
     * @return crow::response
     */
    crow::response multiply_vectors(int id1, int id2);

    /**
     * @brief Method in charge of retrieving the Matrix resources from the DB
     * and adding them.
     *
     * @param id1 - the id of the first Matrix.
     * @param id2 - the id of the second Matrix.
     * @return crow::response
     */
    crow::response add_matrices(int id1, int id2);

    /**
     * @brief Method in charge of retrieving the Matrix resources from the DB
     * and multiplying them.
     *
     * @param id1 - the id of the first Matrix.
     * @param id2 - the id of the second Matrix.
     * @return crow::response
     */
    crow::response multiply_matrices(int id1, int id2);
};

};  // namespace server
}  // namespace rest
}  // namespace ansys

#endif /* SRC_ANSYS_EIGEN_CPP_REST_SERVER_SRC_RESTSERVER_HPP */
