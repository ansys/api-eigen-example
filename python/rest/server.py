import json
import os

import click
import demo_eigen_wrapper
from flask import Flask, jsonify, request
import numpy as np

from python.rest.restdb.db import get_db, init_app_db

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


def create_app():
    """REST API Server initializer.

    Returns
    -------
    Flask
        The instance of our application.

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

    # Teardown previous DB and initialize it!
    init_app_db(app)

    # =================================================================================================
    # PUBLIC METHODS for Server interaction
    # =================================================================================================

    @app.route("/Vectors", methods=["POST"])
    def post_vector():
        """Method which handles the app's (service) behavior when accessing the "Vectors" resource.

        Returns
        -------
        Response
            Response object containing the ID of the recently posted Vector.
        """
        # Perform the POST operation using the general method (to avoid code duplications)
        response_body = __post_eigen_object("vector")

        # Return a successful response with the ID of the created object
        return response_body, 201

    @app.route("/add/Vectors", methods=["GET"])
    def add_vectors():
        """Method which handles the app's (service) behavior when accessing the "addition"
        operation for "Vectors" resource.

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
        """Method which handles the app's (service) behavior when accessing the "multiplication"
        operation for "Vectors" resource.

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
        """Method which handles the app's (service) behavior when accessing the "Matrices" resource

        Returns
        -------
        Response
            Response object containing the ID of the recently posted Matrix
        """
        # Perform the POST operation using the general method (to avoid code duplications)
        response_body = __post_eigen_object("matrix")

        # Return a successful response with the ID of the created object
        return response_body, 201

    @app.route("/add/Matrices", methods=["GET"])
    def add_matrices():
        """Method which handles the app's (service) behavior when accessing the "addition"
        operation for "Matrix" resource.

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
        """Method which handles the app's (service) behavior when accessing the "multiplication"
        operation for "Matrix" resource.

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
        """Server error class for the API REST Server.

        Parameters
        ----------
        Exception : class
            The class from which it inherits

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
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    # =================================================================================================
    # PRIVATE METHODS for Server interaction
    # =================================================================================================

    def __post_eigen_object(type):
        """Private method in charge of inserting one of the possible binded objects of Eigen
        (Vector, Matrix) into the server's DB.

        Parameters
        ----------
        type : parameter
            The type of object to be inserted into the DB. It has to be available within the
            ALLOWED_TYPES tuple and it has to be a string.

        Returns
        -------
        str
            JSON Formatted string which contains the ID of the recently inserted object.

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

        # Finally, announce that the object has been added to the DB and..-
        click.echo(
            str_type.capitalize()
            + " "
            + str_value
            + " has been inserted into the server's DB."
        )

        # ... return the body of the response
        return json.dumps({str_type: {"id": id_in_db}})

    def __ops_eigen_objects(type, ops):
        """Private method in charge of performing a certain operation of the type of
        objects provided.

        Parameters
        ----------
        type : parameter
            The type of object to be considered in the operation. It has to be available
            within the ALLOWED_TYPES tuple and it has to be a string.
        ops : parameter
            The operation to be carried out. It has to be available within the ALLOWED_OPS
            tuple and it has to be a string.

        Returns
        -------
        str
            JSON Formatted string which contains the result of the operation.

        Raises
        ------
        InvalidUsage
            In case no JSON-format request body was provided.
        InvalidUsage
            In case no 'id's are provided within the request body.
        """
        # Check the arguments of this method
        str_type = __check_value(type, ALLOWED_TYPES)
        str_ops = __check_value(ops, ALLOWED_OPS)

        # Retrieve the body of the request silently
        body = request.get_json(silent=True)

        # First check that the request content is in application/json format and
        # that there are at least some contents within.
        if body is None:
            raise InvalidUsage(
                "No JSON-format (i.e. application/json) body was provided in the request."
            )

        # Get the object IDs to be retrieved from the DB
        id1 = body.get("id1", None)
        id2 = body.get("id2", None)

        # Check that the object IDs have been indeed provided in the request body
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
        """Sanity-check method to ensure that the provided value is in the ALLOWED_* tuple
        and it is a string.

        Parameters
        ----------
        value : parameter
            The value to be processed. It has to be available within the ALLOWED_* tuples
            provided and it has to be a string.

        allowed_values : parameter
            The ALLOWED_* tuple to be considered for evaluation.

        Returns
        -------
        str
            The value argument as a string object

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
        """Private method for retrieving the data from the DB and performing a certain
        operation with the eigen-wrapper.

        Parameters
        ----------
        str_type : str
            The type/nature of the objects involved in the operation (i.e. vector, matrix).
        str_ops : str
            The type of operation to be performed (i.e. addition, multiplication).
        id1 : int
            The DB identifier for the first object.
        id2 : int
            The DB identifier for the second object.

        Returns
        -------
        double/List(double)
            The result of the operation.
        """
        # First, get the values from the DB given the ids (as strings)
        db_conn = get_db()
        cur = db_conn.cursor()
        cur.execute(
            "SELECT eigen_value FROM eigen_db WHERE id in (?) AND eigen_type in (?)",
            (id1, str_type.upper()),
        )

        # Ensure that we have retrieved a value for ID1
        try:
            str_value1 = cur.fetchone()[0]
        except TypeError as error:
            click.echo(error)
            raise InvalidUsage(
                "Unexpected error... No values in the DB for id "
                + str(id1)
                + " and type "
                + str_type.capitalize()
                + "."
            )

        cur.execute(
            "SELECT eigen_value FROM eigen_db WHERE id in (?) AND eigen_type in (?)",
            (id2, str_type.upper()),
        )

        # Ensure that we have retrieved a value for ID2
        try:
            str_value2 = cur.fetchone()[0]
        except TypeError as error:
            click.echo(error)
            raise InvalidUsage(
                "Unexpected error... No values in the DB for id "
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

    return app


if __name__ == "__main__":
    # Create the app
    app = create_app()

    # When this script is run, deploy the application in 0.0.0.0:5000
    app.run(host="127.0.0.1", port=5000)
