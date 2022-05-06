#include <crow.h>

#include "RestServer.hpp"
#include "RestDb.hpp"

int main() {
    // We are defining our CROW app
    crow::SimpleApp app;

    // Let us initialize our DB
    sqlite3 *db;
    ansys::rest::db::initialize_db(db);

    // We are defining how we want this endpoint to behave
    CROW_ROUTE(app, "/")
    ([]() {
        return "Greetings from the REST Eigen Server (implemented in C++)!";
    });

    // We define how we want each of the endpoints to behave
    // CROW_ROUTE(app, "/Vectors")
    //     .methods(crow::HTTPMethod::POST)([](const crow::request &req) {
    //         // Check if the request body has
    //         const crow::json::rvalue req_body{crow::json::load(req.body)};

    //         if (req_body.has("id")) {
    //         }

    //         return nullptr;
    //     });

    // We define the app, with its port, and in multi-thread config... and set
    // it to run
    app.port(18080).multithreaded().run();
}
