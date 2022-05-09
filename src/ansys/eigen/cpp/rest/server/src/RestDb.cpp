
#include "RestDb.hpp"

#include <stdio.h>
#include <stdlib.h>

#include <iostream>
#include <stdexcept>

std::string ansys::rest::db::dbtype_to_str(const DbTypes &value) {
    switch (value) {
        // Return enum value VECTOR as a std::string
        case DbTypes::VECTOR:
            return "VECTOR";
        // Return enum value MATRIX as a std::string
        case DbTypes::MATRIX:
            return "MATRIX";
        default:
            throw std::invalid_argument("Invalid argument.");
    }
}

static int ansys::rest::db::callback(void *value, int argc, char **argv,
                                     char **azColName) {
    for (int i = 0; i < argc; i++) {
        printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");

        // Store Value if provided as argument... safe-check cast is performed-
        if (std::string *castedValue = reinterpret_cast<std::string *>(value)) {
            castedValue->assign(argv[i]);
        }
    }

    printf("\n");
    return 0;
}

ansys::rest::db::RestDb::RestDb() {
    fprintf(stdout, "RestDb object created.\n");

    // Initialize the DB
    initialize_db();
}

ansys::rest::db::RestDb::~RestDb() {
    fprintf(stdout, "Destroying RestDb...\n");

    // Close the DB adequately
    sqlite3_close(_db);
}

void ansys::rest::db::RestDb::initialize_db() {
    // Needed variables
    int returnCode;  // return value
    char *zErrMsg;   // error message

    // Start by creating the db
    returnCode = sqlite3_open(nullptr, &_db);

    // Check if the DB has been initialized or not
    if (returnCode) {
        fprintf(stderr, "Can't open database: %s\n", sqlite3_errmsg(_db));
    } else {
        fprintf(stderr, "Opened database successfully.\n");
    }

    // Create SQL statement
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
    returnCode = sqlite3_exec(_db, sql, callback, 0, &zErrMsg);
    if (returnCode != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
    } else {
        fprintf(stdout, "DB tables created successfully.\n");
    }
}

long ansys::rest::db::RestDb::store_resource(const DbTypes &type,
                                             const std::string &input) {
    // Needed variables
    int returnCode;  // return value
    char *zErrMsg;   // error message

    // Create SQL statement
    std::string sql_str =
        "INSERT INTO eigen_db (eigen_type, eigen_value) VALUES ('" +
        ansys::rest::db::dbtype_to_str(type) + "', '" + input + "');";

    // Execute SQL statement
    returnCode = sqlite3_exec(_db, sql_str.c_str(), callback, 0, &zErrMsg);
    if (returnCode != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
        throw std::runtime_error("Insertion unsuccessfull!");
    } else {
        fprintf(stdout,
                "Insertion successfull. Returning ID of inserted row.\n");
        return sqlite3_last_insert_rowid(_db);
    }
}

std::string ansys::rest::db::RestDb::load_resource(const DbTypes &type,
                                                   const int &input) {
    // Needed variables
    int returnCode;  // return value
    char *zErrMsg;   // error message

    // Create SQL statement
    std::string sql_str = "SELECT eigen_value FROM eigen_db WHERE id in (" +
                          std::to_string(input) + ") AND eigen_type in ('" +
                          ansys::rest::db::dbtype_to_str(type) + "');";

    // Execute SQL statement
    std::string value{};
    returnCode = sqlite3_exec(_db, sql_str.c_str(), callback, &value, &zErrMsg);

    // Check the return code... if everything went fine, return the value.
    if (returnCode != SQLITE_OK) {
        fprintf(stderr, "SQL error: %s\n", zErrMsg);
        sqlite3_free(zErrMsg);
        throw std::runtime_error("Search unsuccessfull!");
    } else {
        fprintf(stdout, "Search successfull. Returning value.\n");
        return value;
    }
}