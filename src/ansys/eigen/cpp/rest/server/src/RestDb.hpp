#include <sqlite3.h>

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
 * @brief Method for initializing the REST DB to be used.
 *
 * @param db : a pointer to the sqlite3 DB.
 * @return True if initialization was successful, False otherwise.
 */
bool initialize_db(sqlite3 *db);

/**
 * @brief Callback to be executed after function is complete.
 *
 * @param NotUsed
 * @param argc
 * @param argv
 * @param azColName
 * @return int
 */
static int callback(void *NotUsed, int argc, char **argv, char **azColName);

}  // namespace db

}  // namespace ansys::rest

#endif /* SRC_ANSYS_EIGEN_CPP_REST_SERVER_SRC_RESTDB_HPP */