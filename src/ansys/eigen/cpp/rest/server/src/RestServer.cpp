#include "RestServer.hpp"

#include <stdio.h>

#include "EigenFunctionalities.hpp"
#include "RestDb.hpp"

ansys::rest::server::RestServer::RestServer() {
    CROW_LOG_INFO << "REST Server object instantiated.";

    // We are defining how we want this endpoint to behave
    //
    // GREETING ENDPOINT
    //==================
    CROW_ROUTE(_app, "/")
    ([](const crow::request& req) {
        return "Greetings from the REST Eigen Server (implemented in C++)!";
    });

    // VECTORS RESOURCE - ENDPOINTS
    //=============================
    vector_resource_endpoints();

    // MATRICES RESOURCE - ENDPOINTS
    //==============================
    matrix_resource_endpoints();

    // VECTORS OPS. - ENDPOINTS
    //=========================
    vector_operations_endpoints();

    // MATRICES OPS. - ENDPOINTS
    //==========================
    matrix_operations_endpoints();
}

ansys::rest::server::RestServer::~RestServer() {
    CROW_LOG_INFO << "REST Server object destroyed.";
}

void ansys::rest::server::RestServer::serve(const int port, const bool async,
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

void ansys::rest::server::RestServer::vector_resource_endpoints() {
    // Define how the different "Vectors" resource endpoints should behave
    //
    // 1) ENDPOINT for POSTING VECTORS
    // ===============================
    CROW_ROUTE(_app, "/Vectors")
        .methods(crow::HTTPMethod::POST)([&](const crow::request& req) {
            // Check if the provided input can be processed
            ansys::eigen::read_vector(req.body);

            // Inform the user that the processing was successful
            CROW_LOG_INFO << "Entry successfully processed.";
            CROW_LOG_INFO << "Attempting to store in DB...";

            // Store into the DB and retrieve its ID
            long id =
                _db.store_resource(ansys::rest::db::DbTypes::VECTOR, req.body);

            // Define the response code and message
            CROW_LOG_INFO << "Storage in DB successful. Creating response.";
            auto responseBody = crow::json::wvalue(
                {{"vector", crow::json::wvalue({{"id", id}})}});

            // Send the response
            return crow::response(201, responseBody);
        });

    // 2) ENDPOINT for GETTING VECTORS
    // ===============================
    CROW_ROUTE(_app, "/Vectors(<int>)")
        .methods(crow::HTTPMethod::GET)([&](int id) {
            CROW_LOG_INFO << "Attempting to load resource from DB...";

            // Load from the DB given its ID
            auto resource =
                _db.load_resource(ansys::rest::db::DbTypes::VECTOR, id);

            if (resource.empty()) {
                // Define the response code and message
                CROW_LOG_INFO << "Entry not found. Creating response.";

                // Send the response
                return crow::response(404, "Entry not found");
            } else {
                // Define the response code and message
                CROW_LOG_INFO << "Search in DB successful. Creating response.";

                // Send the response
                return crow::response(200, resource);
            }
        });
}

void ansys::rest::server::RestServer::matrix_resource_endpoints() {
    // Define how the different "Matrices" resource endpoints should behave
    //
    // 1) ENDPOINT for POSTING MATRICES
    // ================================
    CROW_ROUTE(_app, "/Matrices")
        .methods(crow::HTTPMethod::POST)([&](const crow::request& req) {
            // Check if the provided input can be processed
            ansys::eigen::read_matrix(req.body);

            // Inform the user that the processing was successful
            CROW_LOG_INFO << "Entry successfully processed.";
            CROW_LOG_INFO << "Attempting to store in DB...";

            // Store into the DB and retrieve its ID
            long id =
                _db.store_resource(ansys::rest::db::DbTypes::MATRIX, req.body);

            // Define the response code and message
            CROW_LOG_INFO << "Storage in DB successful. Creating response.";
            auto responseBody = crow::json::wvalue(
                {{"matrix", crow::json::wvalue({{"id", id}})}});

            // Send the response
            return crow::response(201, responseBody);
        });

    // 2) ENDPOINT for GETTING MATRICES
    // ================================
    CROW_ROUTE(_app, "/Matrices(<int>)")
        .methods(crow::HTTPMethod::GET)([&](int id) {
            CROW_LOG_INFO << "Attempting to load resource from DB...";

            // Load from the DB given its ID
            auto resource =
                _db.load_resource(ansys::rest::db::DbTypes::MATRIX, id);

            if (resource.empty()) {
                // Define the response code and message
                CROW_LOG_INFO << "Entry not found. Creating response.";

                // Send the response
                return crow::response(404, "Entry not found");
            } else {
                // Define the response code and message
                CROW_LOG_INFO << "Search in DB successful. Creating response.";

                // Send the response
                return crow::response(200, resource);
            }
        });
}

void ansys::rest::server::RestServer::vector_operations_endpoints() {
    // Define how the different "Vectors" operations endpoints should behave
    //
    // 1) ENDPOINT for ADDING VECTORS
    // ==============================
    CROW_ROUTE(_app, "/add/Vectors")
        .methods(crow::HTTPMethod::GET)([&](const crow::request& req) {
            CROW_LOG_INFO << "Attempting to add Vector resources...";
            // Expected request body content to be like...
            // {"id1":1, "id2":2}
            //
            // Check if the request body has the expected inputs
            const crow::json::rvalue json_input = crow::json::load(req.body);
            if (json_input.has("id1") && json_input.has("id2")) {
                return add_vectors(json_input["id1"].i(),
                                   json_input["id2"].i());
            } else {
                // JSON content does not have the expected format
                return crow::response(
                    500, "Expected 'id1','id2' keys in request not present.");
            }
        });

    CROW_ROUTE(_app, "/add/Vectors/<int>/<int>")
        .methods(crow::HTTPMethod::GET)([&](int id1, int id2) {
            CROW_LOG_INFO << "Attempting to add Vector resources...";
            // Expected request body content to be empty
            // However, URL should look like... /add/Vectors/1/2
            //
            // Without request body... but IDs in URL! =)
            //
            return add_vectors(id1, id2);
        });

    // 2) ENDPOINT for MULTIPLYING VECTORS
    // ===================================
    CROW_ROUTE(_app, "/multiply/Vectors")
        .methods(crow::HTTPMethod::GET)([&](const crow::request& req) {
            CROW_LOG_INFO << "Attempting to multiply Vector resources...";
            // Expected request body content to be like...
            // {"id1":1, "id2":2}
            //
            // Check if the request body has the expected inputs
            const crow::json::rvalue json_input = crow::json::load(req.body);
            if (json_input.has("id1") && json_input.has("id2")) {
                return multiply_vectors(json_input["id1"].i(),
                                        json_input["id2"].i());
            } else {
                // JSON content does not have the expected format
                return crow::response(
                    500, "Expected 'id1','id2' keys in request not present.");
            }
        });

    CROW_ROUTE(_app, "/multiply/Vectors/<int>/<int>")
        .methods(crow::HTTPMethod::GET)([&](int id1, int id2) {
            CROW_LOG_INFO << "Attempting to multiply Vector resources...";
            // Expected request body content to be empty
            // However, URL should look like... /multiply/Vectors/1/2
            //
            // Without request body... but IDs in URL! =)
            //
            return multiply_vectors(id1, id2);
        });
}

void ansys::rest::server::RestServer::matrix_operations_endpoints() {
    // Define how the different "Matrices" operations endpoints should behave
    //
    // 1) ENDPOINT for ADDING MATRICES
    // ===============================
    CROW_ROUTE(_app, "/add/Matrices")
        .methods(crow::HTTPMethod::GET)([&](const crow::request& req) {
            CROW_LOG_INFO << "Attempting to add Matrix resources...";
            // Expected request body content to be like...
            // {"id1":1, "id2":2}
            //
            // Check if the request body has the expected inputs
            const crow::json::rvalue json_input = crow::json::load(req.body);
            if (json_input.has("id1") && json_input.has("id2")) {
                return add_matrices(json_input["id1"].i(),
                                    json_input["id2"].i());
            } else {
                // JSON content does not have the expected format
                return crow::response(
                    500, "Expected 'id1','id2' keys in request not present.");
            }
        });

    CROW_ROUTE(_app, "/add/Matrices/<int>/<int>")
        .methods(crow::HTTPMethod::GET)([&](int id1, int id2) {
            CROW_LOG_INFO << "Attempting to add Matrix resources...";
            // Expected request body content to be empty
            // However, URL should look like... /add/Matrices/1/2
            //
            // Without request body... but IDs in URL! =)
            //
            return add_matrices(id1, id2);
        });

    // 2) ENDPOINT for MULTIPLYING MATRICES
    // ====================================
    CROW_ROUTE(_app, "/multiply/Matrices")
        .methods(crow::HTTPMethod::GET)([&](const crow::request& req) {
            CROW_LOG_INFO << "Attempting to multiply Matrix resources...";
            // Expected request body content to be like...
            // {"id1":1, "id2":2}
            //
            // Check if the request body has the expected inputs
            const crow::json::rvalue json_input = crow::json::load(req.body);
            if (json_input.has("id1") && json_input.has("id2")) {
                return multiply_matrices(json_input["id1"].i(),
                                         json_input["id2"].i());
            } else {
                // JSON content does not have the expected format
                return crow::response(
                    500, "Expected 'id1','id2' keys in request not present.");
            }
        });

    CROW_ROUTE(_app, "/multiply/Matrices/<int>/<int>")
        .methods(crow::HTTPMethod::GET)([&](int id1, int id2) {
            CROW_LOG_INFO << "Attempting to multiply Matrix resources...";
            // Expected request body content to be empty
            // However, URL should look like... /multiply/Matrices/1/2
            //
            // Without request body... but IDs in URL! =)
            //
            return multiply_matrices(id1, id2);
        });
}

crow::response ansys::rest::server::RestServer::add_vectors(int id1, int id2) {
    // First, load the resources from the DB (as strings)
    auto s_id1 = _db.load_resource(ansys::rest::db::DbTypes::VECTOR, id1);
    auto s_id2 = _db.load_resource(ansys::rest::db::DbTypes::VECTOR, id2);

    // Now, transform them to Eigen::VectorXd objects
    auto e_id1 = ansys::eigen::read_vector(s_id1);
    auto e_id2 = ansys::eigen::read_vector(s_id2);

    // Once we have the Eigen Vectors, perform the operations
    auto e_res = ansys::eigen::add_vectors(e_id1, e_id2);

    // Now, we will write the resulting vector operation
    auto res = ansys::eigen::write_vector(e_res);

    // And finally, write the response
    CROW_LOG_INFO << "Vector addition operation successful. Creating response.";
    auto responseBody = crow::json::wvalue(
        {{"vector-addition", crow::json::wvalue({{"result", res}})}});

    // Send the response
    return crow::response(200, responseBody);
}

crow::response ansys::rest::server::RestServer::multiply_vectors(int id1,
                                                                 int id2) {
    // First, load the resources from the DB
    auto s_id1 = _db.load_resource(ansys::rest::db::DbTypes::VECTOR, id1);
    auto s_id2 = _db.load_resource(ansys::rest::db::DbTypes::VECTOR, id2);

    // Now, transform them to Eigen::VectorXd objects
    auto e_id1 = ansys::eigen::read_vector(s_id1);
    auto e_id2 = ansys::eigen::read_vector(s_id2);

    // Once we have the Eigen Vectors, perform the operations
    auto e_res = ansys::eigen::multiply_vectors(e_id1, e_id2);

    // And finally, write the response
    CROW_LOG_INFO
        << "Vector multiplication operation successful. Creating response.";
    auto responseBody = crow::json::wvalue(
        {{"vector-multiplication", crow::json::wvalue({{"result", e_res}})}});

    // Send the response
    return crow::response(200, responseBody);
}

crow::response ansys::rest::server::RestServer::add_matrices(int id1, int id2) {
    // First, load the resources from the DB
    auto s_id1 = _db.load_resource(ansys::rest::db::DbTypes::MATRIX, id1);
    auto s_id2 = _db.load_resource(ansys::rest::db::DbTypes::MATRIX, id2);

    // Now, transform them to Eigen::MatrixXd objects
    auto e_id1 = ansys::eigen::read_matrix(s_id1);
    auto e_id2 = ansys::eigen::read_matrix(s_id2);

    // Once we have the Eigen Matrices, perform the operations
    auto e_res = ansys::eigen::add_matrices(e_id1, e_id2);

    // Now, we will write the resulting matrix operation
    auto res = ansys::eigen::write_matrix(e_res);

    // And finally, write the response
    CROW_LOG_INFO << "Matrix addition operation successful. Creating response.";
    auto responseBody = crow::json::wvalue(
        {{"matrix-addition", crow::json::wvalue({{"result", res}})}});

    // Send the response
    return crow::response(200, responseBody);
}

crow::response ansys::rest::server::RestServer::multiply_matrices(int id1,
                                                                  int id2) {
    // First, load the resources from the DB
    auto s_id1 = _db.load_resource(ansys::rest::db::DbTypes::MATRIX, id1);
    auto s_id2 = _db.load_resource(ansys::rest::db::DbTypes::MATRIX, id2);

    // Now, transform them to Eigen::MatrixXd objects
    auto e_id1 = ansys::eigen::read_matrix(s_id1);
    auto e_id2 = ansys::eigen::read_matrix(s_id2);

    // Once we have the Eigen Matrices, perform the operations
    auto e_res = ansys::eigen::multiply_matrices(e_id1, e_id2);

    // Now, we will write the resulting matrix operation
    auto res = ansys::eigen::write_matrix(e_res);

    // And finally, write the response
    CROW_LOG_INFO
        << "Matrix multiplication operation successful. Creating response.";
    auto responseBody = crow::json::wvalue(
        {{"matrix-multiplication", crow::json::wvalue({{"result", res}})}});

    // Send the response
    return crow::response(200, responseBody);
}
