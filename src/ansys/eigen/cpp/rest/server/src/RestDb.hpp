#include <sqlite3.h>

#include <string>

#ifndef SRC_ANSYS_EIGEN_CPP_REST_SERVER_SRC_RESTDB_HPP
#define SRC_ANSYS_EIGEN_CPP_REST_SERVER_SRC_RESTDB_HPP

/**
 * @brief This namespace contains the REST Server logic.
 */
namespace ansys::rest {

/**
 * @brief Namespace for including the REST DB functionalities.
 */
namespace db {

/**
 * @brief Enum holding the types of variables handled.
 */
enum class DbTypes {
    VECTOR,  ///< The Vector type
    MATRIX   ///< The Matrix type
};

/**
 * @brief Method for returning the enum value as a std::string.
 *
 * @param value : the enum value we want as a std::string.
 * @return std::string
 */
std::string dbtype_to_str(const DbTypes &value);

/**
 * @brief Callback to be executed after function is complete.
 *
 * @param value pointer to the argument passed in sqlite3_exec.
 * @param argc number of callbacks to process.
 * @param argv values in each callback.
 * @param azColName name of the cols in the callback.
 * @return int
 */
static int callback(void *value, int argc, char **argv, char **azColName);

/**
 * @brief Class for establishing a connection with the REST DB and interacting
 * with it.
 */
class RestDb {
   public:
    /**
     * @brief Construct a new Rest Db object.
     */
    RestDb();

    /**
     * @brief Destroy the Rest Db object.
     */
    ~RestDb();

    /**
     * @brief Method for storing a Resource in the REST DB.
     *
     * @param type : the type of resource processed.
     * @param input: the JSON request body from where the resource is parsed.
     * @return long : the id of the inserted row in the DB.
     */
    long store_resource(const DbTypes &type, const std::string &input);

    /**
     * @brief Method in charge of loading a stored resource in the DB from a
     * given ID.
     *
     * @param type : the type of resource processed.
     * @param input: the id of the resource inside the DB.
     * @return std::string : the resource loaded from the DB (as a string).
     */
    std::string load_resource(const DbTypes &type, const int &id);

   private:
    /**
     * @brief A pointer to the DB connection.
     */
    sqlite3 *_db;

    /**
     * @brief Method for initializing the REST DB to be used.
     */
    void initialize_db();
};

}  // namespace db

}  // namespace ansys::rest

#endif /* SRC_ANSYS_EIGEN_CPP_REST_SERVER_SRC_RESTDB_HPP */