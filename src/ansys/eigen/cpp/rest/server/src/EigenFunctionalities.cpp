#include "EigenFunctionalities.hpp"

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

    // Get the input string as a C str + its length
    char* ptr = (char*)input.c_str();
    int len = input.length();

    // This is the Vector index
    int idx = 0;

    // Let us start parsing the vector
    char* start = ptr;
    for (int i = 0; i < len; i++) {
        if (ptr[i] == '[') {
            // First entry for parsing --> Vector start
            start = ptr + i + 1;
        } else if (ptr[i] == ']') {
            // We have reached the end! Parse one last time
            res(idx) = atof(start);
        } else if (ptr[i] == ',') {
            // We have reached the end of an entry, parse the value!
            res(idx) = atof(start);
            start = ptr + i + 1;
            idx++;
        }
    }

    // Return the Eigen::VectorXd after resizing
    res.resize(idx + 1);

    return res;
}

Eigen::MatrixXd EigenFunctionalities::read_matrix(const std::string& input) {
    return Eigen::MatrixXd{};
}
