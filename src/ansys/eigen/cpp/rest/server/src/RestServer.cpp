#include "RestServer.hpp"

#include <stdio.h>

#include "EigenFunctionalities.hpp"

ansys::rest::RestServer::RestServer(sqlite3* db) : _db(db) {
    fprintf(stdout, "REST Server object instantiated\n");

    // We are defining how we want this endpoint to behave
    //
    // GREETING ENDPOINT
    //==================
    CROW_ROUTE(_app, "/")
    ([](const crow::request& req) {
        return "Greetings from the REST Eigen Server (implemented in C++)!";
    });

    // VECTORS ENDPOINT
    //==================
    CROW_ROUTE(_app, "/Vectors")
        .methods(crow::HTTPMethod::POST)([](const crow::request& req) {
            // Check if the request body has the expected inputs
            const crow::json::rvalue req_body{crow::json::load(req.body)};

            if (req_body.has("value")) {
                // TODO (rpastorm): we have to process the vector...
                // std::string value = req_body["value"];
                // auto e_value = EigenFunctionalities::read_vector(value);
            }

            // TODO (rpastorm): This ID will have to be received from the DB
            int id = 0;

            // Define the response code and message
            auto responseBody = crow::json::wvalue(
                {{"vector", crow::json::wvalue({{"id", id}})}});
            return crow::response(201, responseBody);
        });
}

ansys::rest::RestServer::~RestServer() {
    fprintf(stdout, "REST Server object destroyed\n");
}

void ansys::rest::RestServer::serve(const int port, const bool async,
                                    const crow::LogLevel logLevel) {
    // Set the servers logging level we have decided
    _app.loglevel(logLevel);

    // Now, serve depending on whether we want it to run asynchronously or not
    // We define the app, with its port, and in multi-thread config... and set
    // it to run accordingly!
    if (async) {
        _app.port(port).multithreaded().run();
    } else {
        _app.port(port).multithreaded().run_async();
    }
}
