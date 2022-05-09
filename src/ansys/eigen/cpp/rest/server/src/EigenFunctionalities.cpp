#include "EigenFunctionalities.hpp"

#include <crow.h>

Eigen::MatrixXd EigenFunctionalities::multiply_matrices(
    const Eigen::MatrixXd& a, const Eigen::MatrixXd& b) {
    return a * b;
}

Eigen::MatrixXd EigenFunctionalities::add_matrices(const Eigen::MatrixXd& a,
                                                   const Eigen::MatrixXd& b) {
    return a + b;
}

double EigenFunctionalities::multiply_vectors(const Eigen::VectorXd& v,
                                              const Eigen::VectorXd& w) {
    return v.dot(w);
}

Eigen::VectorXd EigenFunctionalities::add_vectors(const Eigen::VectorXd& v,
                                                  const Eigen::VectorXd& w) {
    return v + w;
}

Eigen::VectorXd EigenFunctionalities::read_vector(const std::string& input) {
    // Initialize our resulting vector
    Eigen::VectorXd res{};

    // Check if the request body has the expected inputs
    const crow::json::rvalue json_input = crow::json::load(input);

    // Check if the provided input can be processed
    if (json_input.has("value")) {
        try {
            // Read the string as a JSON
            const crow::json::rvalue value = json_input["value"];

            // Resize our Eigen::VectorXd to the provided size
            res.resize(value.size());

            // Process the entries! Expected entries are of type double (or int,
            // but castable)...
            int idx{0};
            for (const auto& val : value) {
                res(idx) = val.d();
            }
        } catch (const std::runtime_error& e) {
            throw std::runtime_error("Error parsing input as vector: " + input +
                                     ".");
        }
    } else {
        // JSON content does not have the expected format
        throw std::runtime_error(
            "Expected 'value' key in request content not present.");
    }

    // Return the Eigen::VectorXd
    return res;
}

Eigen::MatrixXd EigenFunctionalities::read_matrix(const std::string& input) {
    // Initialize our resulting vector
    Eigen::MatrixXd res{};

    // Check if the request body has the expected inputs
    const crow::json::rvalue json_input = crow::json::load(input);

    // Check if the provided input can be processed
    if (json_input.has("value")) {
        try {
            // Read the string as a JSON
            const crow::json::rvalue value = json_input["value"];

            // Process the entries! Expected entries are of type double (or int,
            // but castable)...
            bool first_time{true};  // Boolean to do some first time processings
            int row_idx{0};         // Idx for row insertion
            int len_cols{0};  // Int holding the expected number of columns in
                              // all rows (to be initialized later on)

            // Loop over matrix rows
            for (const auto& row : value) {
                // Do this only once
                if (first_time) {
                    // Resize the matrix to its adequate form...
                    res.resize(value.size(), row.size());
                    // ...and store the maximum size of the columns
                    len_cols = row.size();
                    // Reset the boolean to false
                    first_time = false;
                }

                if (len_cols != row.size()) {
                    throw std::runtime_error(
                        "Invalid matrix. Column sizes are variable.");
                }

                // Initialize the column index
                int col_idx{0};

                // Loop over entries in a row
                for (const auto& val : row) {
                    res(row_idx, col_idx) = val.d();
                }
            }
        } catch (const std::runtime_error& e) {
            throw std::runtime_error("Error parsing input as matrix: " + input +
                                     ".");
        }
    } else {
        // JSON content does not have the expected format
        throw std::runtime_error(
            "Expected 'value' key in request content not present.");
    }

    // Return the Eigen::MatrixXd
    return res;
}
