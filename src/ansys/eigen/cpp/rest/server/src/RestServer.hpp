#include <crow.h>
#include <sqlite3.h>

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
     * @brief Construct a new Rest Server object
     *
     * @param db : the database to be used for storing the resources.
     */
    RestServer(sqlite3* db);

    /**
     * @brief Destroy the Rest Server object.
     */
    ~RestServer();

    /**
     * @brief Method for serving our application.
     *
     * @param port : the port in which we want to server our app. Default:
     * 18080.
     * @param async : whether we want to run application asynchronously or not.
     * Default: false.
     * @param logLevel : the logging level of our server. Default: Info.
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
     * @brief A pointer to our server's DB.
     */
    sqlite3* _db;

    /**
     * @brief The server CROW application.
     */
    crow::SimpleApp _app;
};

};  // namespace ansys::rest

#endif /* SRC_ANSYS_EIGEN_CPP_REST_SERVER_SRC_RESTSERVER_HPP */
