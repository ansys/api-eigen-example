# Copyright (C) 2023 - 2026 ANSYS, Inc. and/or its affiliates.
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

"""Python implementation of the REST API Eigen example database."""

import os
import sqlite3

import click
from flask import current_app, g

# =================================================================================================
# PUBLIC METHODS for DB interaction
# =================================================================================================


def init_app_db(app):
    """Initialize a simple database for storing API REST data."""
    current_app = app
    current_app.app_context().push()

    # Initialize the new app's DB, deleting any pre-existing data and build it from scracth
    __init_db()

    # Register this function so that it is called whenever a response is returned by the application
    current_app.teardown_appcontext(__close_db)

    # Emit a message informing the user
    click.echo("Our App's DB has been initialized!")


def get_db():
    """Get the database instance of the Flask app.

    Returns
    -------
    Connection
        Connection to the app's database.
    """
    if "db" not in g:
        # Check if folder exists... otherwise, create it
        os.makedirs(os.path.dirname(current_app.config["DATABASE"]), exist_ok=True)

        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# =================================================================================================
# PRIVATE METHODS for DB interaction
# =================================================================================================


def __close_db(*args):
    """Close the database."""
    db = g.pop("db", None)

    if db is not None:
        db.close()


def __init_db():
    """Initialize the database."""
    db = get_db()

    with current_app.open_resource("restdb/schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
