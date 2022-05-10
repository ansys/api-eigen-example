#include <crow.h>

#include "RestDb.hpp"

#ifndef SRC_ANSYS_EIGEN_CPP_REST_SERVER_SRC_RESTSERVER_HPP
#define SRC_ANSYS_EIGEN_CPP_REST_SERVER_SRC_RESTSERVER_HPP

/**
 * @brief This namespace contains the REST Server logic.
 */
namespace ansys::rest {

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
};

};  // namespace ansys::rest

#endif /* SRC_ANSYS_EIGEN_CPP_REST_SERVER_SRC_RESTSERVER_HPP */
