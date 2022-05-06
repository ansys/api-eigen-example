
#include "RestDb.hpp"

#include <stdio.h>
#include <stdlib.h>

bool ansys::rest::db::initialize_db(sqlite3 *db) {
    // Needed variables
    int rc;         // return value
    char *zErrMsg;  // Error message

    // Start by creating the db
    rc = sqlite3_open(nullptr, &db);

    // Check if the DB has been initialized or not
    if (rc) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(db));
        return false;
    } else {
        fprintf(stderr, "Opened database successfully\n");
    }

    /* Create SQL statement */
    const char *sql =
        "DROP TABLE IF EXISTS eigen_db;"
        "DROP TABLE IF EXISTS types;"
        "CREATE TABLE types (eigen_type TEXT NOT NULL, PRIMARY KEY "
        "(eigen_type));"
        "CREATE TABLE eigen_db (id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "eigen_type TEXT NOT NULL, eigen_value TEXT NOT NULL,FOREIGN KEY "
        "(eigen_type) REFERENCES types (eigen_type));"
        "INSERT INTO types (eigen_type) VALUES ('VECTOR');"
        "INSERT INTO types (eigen_type) VALUES ('MATRIX');";

    // Execute SQL statement - for initializing DB tables
    rc = sqlite3_exec(db, sql, callback, 0, &zErrMsg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
        return false;
    } else {
        fprintf(stdout, "Records created successfully\n");
        return true;
    }
}

static int ansys::rest::db::callback(void *NotUsed, int argc, char **argv, char **azColName) {
    int i;
    for (i = 0; i < argc; i++) {
        printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
    }

    printf("\n");
    return 0;
}