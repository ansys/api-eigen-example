#include <eigen3/Eigen/Dense>

#ifndef SRC_ANSYS_EIGEN_CPP_REST_SERVER_SRC_EIGENFUNCTIONALITIES_HPP
#define SRC_ANSYS_EIGEN_CPP_REST_SERVER_SRC_EIGENFUNCTIONALITIES_HPP

namespace EigenFunctionalities {
/**
 * @brief Wrapper method to Matrix multiplication carried out by Eigen
 * operators.
 *
 * @param a The first matrix.
 * @param b The second matrix.
 *
 * @return Eigen::MatrixXd
 */
Eigen::MatrixXd multiply_matrices(const Eigen::MatrixXd& a,
                                  const Eigen::MatrixXd& b);

/**
 * @brief Wrapper method to Matrix addition carried out by Eigen operators.
 *
 * @param a The first matrix.
 * @param b The second matrix.
 *
 * @return Eigen::MatrixXd
 */
Eigen::MatrixXd add_matrices(const Eigen::MatrixXd& a,
                             const Eigen::MatrixXd& b);

/**
 * @brief Wrapper method to Vector multiplication (dot product) carried out by
 * Eigen operators.
 *
 * @param v The first vector.
 * @param w The second vector.
 *
 * @return double
 */
double multiply_vectors(const Eigen::VectorXd& v, const Eigen::VectorXd& w);

/**
 * @brief Wrapper method to Vector addition carried out by Eigen operators.
 *
 * @param v The first vector.
 * @param w The second vector.
 *
 * @return Eigen::VectorXd
 */
Eigen::VectorXd add_vectors(const Eigen::VectorXd& v, const Eigen::VectorXd& w);

/**
 * @brief Method in charge of parsing the JSON list to a vector.
 * 
 * @param input : the JSON list.
 * @return Eigen::VectorXd 
 */
Eigen::VectorXd read_vector(const std::string& input);

/**
 * @brief Method in charge of parsing the JSON list of lists to a matrix.
 * 
 * @param input : the JSON list of lists.
 * @return Eigen::MatrixXd 
 */
Eigen::MatrixXd read_matrix(const std::string& input);

/**
 * @brief Method in charge of writing a JSON list from the Eigen::VectorXd object given.
 * 
 * @param input : the Eigen::VectorXd.
 * @return std::string representing the Vector as a JSON list 
 */
std::string write_vector(const Eigen::VectorXd& input);

/**
 * @brief Method in charge of writing a JSON list from the Eigen::MatrixXd object given.
 * 
 * @param input : the Eigen::MatrixXd.
 * @return std::string representing the Matrix as a JSON list 
 */
std::string write_matrix(const Eigen::MatrixXd& input);

}  // namespace EigenFunctionalities

#endif /* SRC_ANSYS_EIGEN_CPP_REST_SERVER_SRC_EIGENFUNCTIONALITIES_HPP */
