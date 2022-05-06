#include "RestDb.hpp"
#include "RestServer.hpp"

int main() {
    // Let us initialize our DB
    sqlite3 *db;
    ansys::rest::db::initialize_db(db);

    // Let us instantiate our server
    ansys::rest::RestServer server{db};

    // Start serving!
    server.serve();
}
