import json
import os
from io import UnsupportedOperation
from typing import List

import click
import numpy as np
from flask import Flask, request

from restdb.db import get_db, init_app_db


def create_app():
    """REST API Server initializer.

    Returns
    -------
    Flask
        The instance of our application.

    Raises
    ------
    RuntimeError
        In case no JSON-format request body was provided.
    RuntimeError
        In case no 'value' is provided within the request body.
        UnsupportedOperation
            In case the given argument is not a string.
        UnsupportedOperation
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

    # When this script is run, deploy the application in 0.0.0.0:5000
    app.run(host="0.0.0.0", port=5000)

    ALLOWED_TYPES = (
        "vector",
        "matrix",
    )

    # =================================================================================================
    # PUBLIC METHODS for Server interaction
    # =================================================================================================

    @app.route("/Vectors", methods=["POST"])
    def post_vector():
        """Method which handles the app's (service) behavior when accessing the "Vectors" resource

        Returns
        -------
        Response
            Response object containing the ID of the recently posted Vector
        """
        # Perform the POST operation using the general method (to avoid code duplications)
        response_body = __post_eigen_object("vector")

        # Return a successful response with the ID of the created object
        return response_body, 201

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
        RuntimeError
            In case no JSON-format request body was provided.
        RuntimeError
            In case no 'value' is provided within the request body.
        """
        # Check the argument of this method
        str_type = __check_type(type)

        # Retrieve the body of the request silently
        body = request.get_json(silent=True)

        # First check that the request content is in application/json format and
        # that there are at least some contents within.
        if body is None:
            raise RuntimeError(
                "No JSON-format (i.e. application/json) body was provided in the request."
            )

        # Get the object to be inserted into the DB
        value = body.get("value", None)

        # Check that the object has been indeed provided in the request body
        if value is None:
            raise RuntimeError(
                "No " + str_type + " has been provided. Expected key: 'value'"
            )

        # Check that the recently parsed "value" can be transformed into a numpy nd.array...
        # Otherwise, throw exception
        try:
            np.array(value, dtype=float)
        except ValueError as error:
            click.echo(error)
            click.echo(
                "Error encountered when transforming input string into numpy nd.array"
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

    def __check_type(type):
        """Sanity-check method to ensure that the provided type is in the ALLOWED_TYPES tuple
        and it is a string.

        Parameters
        ----------
        type : parameter
            The type of object to be inserted into the DB. It has to be available within the
            ALLOWED_TYPES tuple and it has to be a string.

        Returns
        -------
        str
            The type argument as a string object

        Raises
        ------
        UnsupportedOperation
            In case the given argument is not a string.
        UnsupportedOperation
            In case the given type is not in the ALLOWED_TYPES tuple.
        """
        # Check that the provided input is a string
        if isinstance(type, str) == False:
            raise UnsupportedOperation(
                "The input to __post_eigen_object(...) should be a str. Check your implementation."
            )

        # Work with the "type" arg as a str object
        str_type = str(type)

        # Check as well that the provided type is one of the allowed types
        if type not in ALLOWED_TYPES:
            raise UnsupportedOperation(
                type.capitalize() + " is not one of the allowed types."
            )

        # Return as a str object
        return str_type

    return app
