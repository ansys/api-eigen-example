#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <apieigen/grpc/GRPCClient.hpp>
#include <apieigen/rest/EigenClient.hpp>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

namespace py = pybind11;

using namespace ansys::grpc::client;
using namespace ansys::rest::client;

PYBIND11_MODULE(eigen_cpp_client, m) {
    m.doc() = R"pbdoc(
        Pybind11 eigen_cpp_client wrapper
        ---------------------------------

        .. currentmodule:: eigen_cpp_client

        .. autosummary::
           :toctree: _generate

           GRPCClient
           RESTClient
    )pbdoc";

    py::class_<GRPCClient>(m, "GRPCClient")
        .def(py::init<const std::string &, const int &>())
        .def("request_greeting", &GRPCClient::request_greeting,
             R"pbdoc(Request a greeting)pbdoc")
        .def("flip_vector", &GRPCClient::flip_vector,
             R"pbdoc(Flip a vector)pbdoc")
        .def("add_vectors", &GRPCClient::add_vectors,
             R"pbdoc(Add two vectors)pbdoc")
        .def("multiply_vectors", &GRPCClient::multiply_vectors,
             R"pbdoc(Multiply two vectors)pbdoc")
        .def("add_matrices", &GRPCClient::add_matrices,
             R"pbdoc(Add two matrices)pbdoc")
        .def("multiply_matrices", &GRPCClient::multiply_matrices,
             R"pbdoc(Multiply two matrices)pbdoc");

    py::class_<EigenClient>(m, "RESTClient")
        .def(py::init<const std::string &>())
        .def("request_greeting", &EigenClient::request_greeting,
             R"pbdoc(Request a greeting)pbdoc")
        .def("add_vectors", &EigenClient::add_vectors,
             R"pbdoc(Add two vectors)pbdoc")
        .def("multiply_vectors", &EigenClient::multiply_vectors,
             R"pbdoc(Multiply two vectors)pbdoc")
        .def("add_matrices", &EigenClient::add_matrices,
             R"pbdoc(Add two matrices)pbdoc")
        .def("multiply_matrices", &EigenClient::multiply_matrices,
             R"pbdoc(Multiply two matrices)pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}
