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
    return Eigen::MatrixXd{};
}
