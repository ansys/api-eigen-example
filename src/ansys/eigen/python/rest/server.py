# Copyright (C) 2023 - 2025 ANSYS, Inc. and/or its affiliates.
# SPDX-License-Identifier: MIT
#
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Python implementation of the REST API Eigen example server."""

import json
from math import floor
import os

import click
import demo_eigen_wrapper
from flask import Flask, jsonify, request
import numpy as np

from ansys.eigen.python.rest.restdb.db import get_db, init_app_db

#
#
# It is necessary to define the environment variable FLASK_APP pointing to this same file
#
# For running the app, just call "flask run"
#
#

# It would be ideal that Python had switches implemented...
# ... specially for these constant parameters
ALLOWED_TYPES = (
    "vector",
    "matrix",
)

ALLOWED_OPS = (
    "addition",
    "multiplication",
)

HUMAN_SIZES = ["B", "KB", "MB", "GB", "TB"]


def create_app():
    """Initialize the REST API server.

    Returns
    -------
    Flask
        Instance of the application.

    Raises
    ------
    InvalidUsage
        In case no JSON-format request body was provided.
    InvalidUsage
        In case no 'value' is provided within the request body.
    InvalidUsage
        In case the given argument is not a string.
    InvalidUsage
        In case the given type is not in the ALLOWED_TYPES tuple.
    """
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "app.sqlite"),
    )

    # Tear down previous database and initialize it
    init_app_db(app)

    # =================================================================================================
    # PUBLIC METHODS for Server interaction
    # =================================================================================================

    @app.route("/Vectors", methods=["POST"])
    def post_vector():
        """Handles the app's (service's) behavior when accessing the ``Vectors`` resource.

        Returns
        -------
        Response
            Response object containing the ID of the recently posted vector.
        """
        # Perform the POST operation using the general method (to avoid code duplications)
        response_body = __post_eigen_object("vector")

        # Return a successful response with the ID of the created object
        return response_body, 201

    @app.route("/add/Vectors", methods=["GET"])
    def add_vectors():
        """Handles the app's (service's) behavior when accessing the addition
        operation for the ``Vectors`` resource.

        Returns
        -------
        Response
            Response object containing the vector operation requested.
        """
        # Perform the GET operation using the general method (to avoid code duplications)
        response_body = __ops_eigen_objects("vector", "addition")

        # Return a successful response with the ID of the created object
        return response_body, 200

    @app.route("/multiply/Vectors", methods=["GET"])
    def multiply_vectors():
        """Handles the app's (service's) behavior when accessing the multiplication
        operation for the ``Vectors`` resource.

        Returns
        -------
        Response
            Response object containing the vector operation requested.
        """
        # Perform the GET operation using the general method (to avoid code duplications)
        response_body = __ops_eigen_objects("vector", "multiplication")

        # Return a successful response with the ID of the created object
        return response_body, 200

    @app.route("/Matrices", methods=["POST"])
    def post_matrix():
        """Handles the app's (service's) behavior when accessing the ``Matrices`` resource

        Returns
        -------
        Response
            Response object containing the ID of the recently posted matrix.
        """
        # Perform the POST operation using the general method (to avoid code duplications)
        response_body = __post_eigen_object("matrix")

        # Return a successful response with the ID of the created object
        return response_body, 201

    @app.route("/add/Matrices", methods=["GET"])
    def add_matrices():
        """Handles the app's (service's) behavior when accessing the addition
        operation for the ``Matrix`` resource.

        Returns
        -------
        Response
            Response object containing the vector operation requested.
        """
        # Perform the GET operation using the general method (to avoid code duplications)
        response_body = __ops_eigen_objects("matrix", "addition")

        # Return a successful response with the ID of the created object
        return response_body, 200

    @app.route("/multiply/Matrices", methods=["GET"])
    def multiply_matrices():
        """Handles the app's (service's) behavior when accessing the multiplication
        operation for the ``Matrix`` resource.

        Returns
        -------
        Response
            Response object containing the matrix operation requested.
        """
        # Perform the GET operation using the general method (to avoid code duplications)
        response_body = __ops_eigen_objects("matrix", "multiplication")

        # Return a successful response with the ID of the created object
        return response_body, 200

    class InvalidUsage(Exception):
        """Provides the server error class for the API REST server.

        Parameters
        ----------
        Exception : class
            Class from which it inherits.

        Returns
        -------
        InvalidUsage
            Internal server error.
        """

        status_code = 400

        def __init__(self, message, status_code=None, payload=None):
            Exception.__init__(self)
            self.message = message
            if status_code is not None:
                self.status_code = status_code
            self.payload = payload

        def to_dict(self):
            rv = dict(self.payload or ())
            rv["message"] = self.message
            return rv

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        """Handles error messages for generating adequate HTTP responses.

        Parameters
        ----------
        error : InvalidUsage
            Incoming error that has been raised.

        Returns
        -------
        Response
            HTTP response with the error information and associated status code.
        """

        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # =================================================================================================
    # PRIVATE METHODS for Server interaction
    # =================================================================================================

    def __post_eigen_object(type):
        """Inserts a possible binded object of Eigen (vector or matrix) into the server's database.

        Parameters
        ----------
        type : parameter
            Type of object to insert into the database. It has to be available within the
            ``ALLOWED_TYPES`` tuple and to be a string.

        Returns
        -------
        str
            JSON-formatted string that contains the ID of the recently inserted object.

        Raises
        ------
        InvalidUsage
            In case no JSON-format request body was provided.
        InvalidUsage
            In case no 'value' is provided within the request body.
        InvalidUsage
            In case an error was encountered when transforming 'value' into numpy.ndarray.
        """
        # Check the argument of this method
        str_type = __check_value(type, ALLOWED_TYPES)

        # Retrieve the body of the request silently
        body = request.get_json(silent=True)

        # First check that the request content is in application/json format and
        # that there are at least some contents within.
        if body is None:
            raise InvalidUsage(
                "No JSON-format (i.e. application/json) body was provided in the request."
            )

        # Get the object to be inserted into the DB
        value = body.get("value", None)

        # Check that the object has been indeed provided in the request body
        if value is None:
            raise InvalidUsage(
                "No " + str_type + " has been provided. Expected key: 'value'."
            )

        # Check that the recently parsed "value" can be transformed into a numpy.ndarray...
        # Otherwise, throw exception
        try:
            np.array(value, dtype=np.float64)
        except ValueError as error:
            click.echo(error)
            raise InvalidUsage(
                "Error encountered when transforming input string into numpy.ndarray."
            )

        # Store the value as a string inside the database
        str_value = json.dumps(value)

        # Insert into DB (as a string) and retrieve the ID of the inserted element
        db_conn = get_db()
        cur = db_conn.cursor()
        cur.execute(
            "INSERT INTO eigen_db(eigen_type, eigen_value) VALUES (?, ?)",
            (str_type.upper(), str_value),
        )
        db_conn.commit()
        id_in_db = cur.lastrowid

        # Announce that the object has been added to the DB and..-
        click.echo(
            str_type.capitalize()
            + " with id "
            + str(id_in_db)
            + " has been inserted into the server's DB."
        )

        # Inform about the size of the message content
        click.echo("Size of message: " + __human_size(request.content_length))

        # ... return the body of the response
        return json.dumps({str_type: {"id": id_in_db}})

    def __ops_eigen_objects(type, ops):
        """Handles performing a certain operation on the type of objects provided.

        Parameters
        ----------
        type : parameter
            Type of object to consider in the operation. It has to be available
            within the ``ALLOWED_TYPES`` tuple and to be a string.
        ops : parameter
            Operation to carry out. It has to be available within the ``ALLOWED_OPS``
            tuple and to be a string.

        Returns
        -------
        str
            JSON-formatted string that contains the result of the operation.

        Raises
        ------
        InvalidUsage
            In case no JSON-format request body was provided.
        InvalidUsage
            In case no IDs are provided within the request body.
        """
        # Check the arguments of this method
        str_type = __check_value(type, ALLOWED_TYPES)
        str_ops = __check_value(ops, ALLOWED_OPS)

        # Retrieve the body of the request silently
        body = request.get_json(silent=True)

        # Check that the request content is in application/json format and
        # that there are at least some contents within.
        if body is None:
            raise InvalidUsage(
                "No JSON-format (i.e. application/json) body was provided in the request."
            )

        # Get the object IDs to be retrieved from the DB
        id1 = body.get("id1", None)
        id2 = body.get("id2", None)

        # Check that the object IDs have been provided in the request body
        if id1 is None or id2 is None:
            raise InvalidUsage(
                "Arguments for "
                + str_ops
                + " operation with "
                + str_type
                + " are not provided. Expected keys: 'id1', 'id2'."
            )

        # Once the inputs have been verified... perform the operation
        value = __perform_operation(str_type, str_ops, id1, id2)

        # ... and return the body of the response
        return json.dumps({str_type + "-" + str_ops: {"result": value}})

    def __check_value(value, allowed_values):
        """Check to ensure that the provided value is in the ``ALLOWED_*`` tuple
        and that it is a string.

        Parameters
        ----------
        value : parameter
            Value to process. It has to be available within the ``ALLOWED_*`` tuples
            provided and has to be a string.

        allowed_values : parameter
            ``ALLOWED_*`` tuple to consider for evaluation.

        Returns
        -------
        str
            Value argument as a string object.

        Raises
        ------
        InvalidUsage
            In case the given argument is not a string.
        InvalidUsage
            In case the given type is not in the ALLOWED_* tuple.
        """
        # Check that the provided input is a string
        if isinstance(value, str) == False:
            raise InvalidUsage(
                "The input to __check_value(...) should be a str. Check your implementation."
            )

        # Work with the "value" arg as a str object
        str_value = str(value)

        # Check as well that the provided value is one of the allowed values
        if str_value not in allowed_values:
            raise InvalidUsage(
                str_value.capitalize()
                + " is not one of the allowed values (i.e. ["
                + ", ".join(allowed_values)
                + "])."
            )

        # Return as a str object
        return str_value

    def __perform_operation(str_type, str_ops, id1, id2):
        """Retrieve the data from the database DB for performing a certain
        operation with the eigen-wrapper.

        Parameters
        ----------
        str_type : str
            Type of the objects involved in the operation (vector or matrix).
        str_ops : str
            Type of operation to perform. For example, addition or multiplication.
        id1 : int
            Dataase identifier for the first object.
        id2 : int
            Database identifier for the second object.

        Returns
        -------
        double/List(double)
            Result of the operation.
        """
        # Get the values from the DB given the ids (as strings)
        db_conn = get_db()
        cur = db_conn.cursor()
        cur.execute(
            "SELECT eigen_value FROM eigen_db WHERE id in (?) AND eigen_type in (?)",
            (id1, str_type.upper()),
        )

        # Ensure that a value is retrieved for ID1
        try:
            str_value1 = cur.fetchone()[0]
        except TypeError as error:
            click.echo(error)
            raise InvalidUsage(
                "Unexpected error... No values in the database for ID "
                + str(id1)
                + " and type "
                + str_type.capitalize()
                + "."
            )

        cur.execute(
            "SELECT eigen_value FROM eigen_db WHERE id in (?) AND eigen_type in (?)",
            (id2, str_type.upper()),
        )

        # Ensure that a value is retrieved for ID2
        try:
            str_value2 = cur.fetchone()[0]
        except TypeError as error:
            click.echo(error)
            raise InvalidUsage(
                "Unexpected error... No values in the database for ID "
                + str(id2)
                + " and type "
                + str_type.capitalize()
                + "."
            )

        # Now, convert to np.arrays
        value1 = np.array(json.loads(str_value1), dtype=np.float64)
        value2 = np.array(json.loads(str_value2), dtype=np.float64)

        # And finally... perform operation
        if str_type == "vector" and str_ops == "addition":
            return demo_eigen_wrapper.add_vectors(value1, value2).tolist()
        elif str_type == "vector" and str_ops == "multiplication":
            return demo_eigen_wrapper.multiply_vectors(value1, value2)
        elif str_type == "matrix" and str_ops == "addition":
            return demo_eigen_wrapper.add_matrices(value1, value2).tolist()
        elif str_type == "matrix" and str_ops == "multiplication":
            return demo_eigen_wrapper.multiply_matrices(value1, value2).tolist()
        else:
            # This should not occur
            return None

    def __human_size(content_length: int):
        """Show the size of the message in human-readable format.

        Parameters
        ----------
        content_length : int
            Content length of the message.

        Returns
        -------
        str
            Size of the message in human-readable format.
        """
        idx = 0
        while True:
            if content_length >= 1024:
                idx += 1
                content_length = floor(content_length / 1024)
            else:
                break

        if idx >= len(HUMAN_SIZES):
            raise InvalidUsage("Message content above TB level... is not handled.")

        return str(content_length) + HUMAN_SIZES[idx]

    return app


if __name__ == "__main__":
    # Create the app
    app = create_app()

    # When this script is run, deploy the application in 0.0.0.0:5000
    app.run(host="127.0.0.1", port=5000)
