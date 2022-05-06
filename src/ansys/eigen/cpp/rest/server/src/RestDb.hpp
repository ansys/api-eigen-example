#include <sqlite3.h>

/**
 * @brief Namespace for including the REST DB functionalities
 */
namespace ansys::rest::db {

/**
 * @brief Method for initializing the REST DB to be used.
 *
 * @param db : a pointer to the sqlite3 db.
 * @return True if initialization was successful, False otherwise.
 */
bool initialize_db(sqlite3 *db);

/**
 * @brief Callback to be executed after function is complete
 *
 * @param NotUsed
 * @param argc
 * @param argv
 * @param azColName
 * @return int
 */
static int callback(void *NotUsed, int argc, char **argv, char **azColName);

}  // namespace ansys::rest::db