#include <pybind11/eigen.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

// It is needed to use type py::EigenDRef<Eigen::MatrixXd> for matrix operations, since numpy arrays are
// characterized for ordering its values differently to Eigen.
//
// Ideally, and for performance reasons, we should avoid using Dynamic MAtrixTypes, to take advantage of
// the vectorization Eigen does when solving matrix operations.

/**
 * @brief Wrapper method to Matrix multiplication carried out by Eigen operators.
 *
 * @param a The first matrix.
 * @param b The second matrix.
 *
 * @return Eigen::MatrixXd
 */
Eigen::MatrixXd multiply_matrices(const py::EigenDRef<Eigen::MatrixXd> a, const py::EigenDRef<Eigen::MatrixXd> b)
{
    return a * b;
}

/**
 * @brief Wrapper method to Matrix addition carried out by Eigen operators.
 *
 * @param a The first matrix.
 * @param b The second matrix.
 *
 * @return Eigen::MatrixXd
 */
Eigen::MatrixXd add_matrices(const py::EigenDRef<Eigen::MatrixXd> a, const py::EigenDRef<Eigen::MatrixXd> b)
{
    return a + b;
}

/**
 * @brief Wrapper method to Vector multiplication (dot product) carried out by Eigen operators.
 *
 * @param v The first vector.
 * @param w The second vector.
 *
 * @return double
 */
double multiply_vectors(const Eigen::Ref<Eigen::VectorXd> v, const Eigen::Ref<Eigen::VectorXd> w)
{
    return v.dot(w);
}

/**
 * @brief Wrapper method to Vector addition carried out by Eigen operators.
 *
 * @param v The first vector.
 * @param w The second vector.
 *
 * @return Eigen::VectorXd
 */
Eigen::VectorXd add_vectors(const Eigen::Ref<Eigen::VectorXd> v, const Eigen::Ref<Eigen::VectorXd> w)
{
    return v + w;
}

PYBIND11_MODULE(demo_eigen_wrapper, m)
{
    m.doc() = R"pbdoc(
        Pybind11 example eigen-wrapper
        ------------------------------

        .. currentmodule:: demo_eigen_wrapper

        .. autosummary::
           :toctree: _generate

           multiply_matrices
           add_matrices
           multiply_vectors
           add_vectors
    )pbdoc";

    m.def("add_vectors", &add_vectors, R"pbdoc(
        Add two Eigen::VectorXd
    )pbdoc");

    m.def("add_matrices", &add_matrices, R"pbdoc(
        Add two Eigen::MatrixXd
    )pbdoc");

    m.def("multiply_vectors", &multiply_vectors, R"pbdoc(
        Dot product of two Eigen::VectorXd
    )pbdoc");

    m.def("multiply_matrices", &multiply_matrices, R"pbdoc(
        Multiply two Eigen::MatrixXd
    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
