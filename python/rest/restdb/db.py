import sqlite3

import click
from flask import current_app, g

# =================================================================================================
# PUBLIC METHODS for DB interaction
# =================================================================================================


def init_app_db(app):
    """Initializer method of a simple DB for storing API REST data."""
    current_app = app
    current_app.app_context().push()

    # We initialize the new App's DB - delete any pre-existing data and build it from scracth
    __init_db()

    # Register this function so that it is called whenever a response is returned by the application
    current_app.teardown_appcontext(__close_db)

    # Emit a message informing the user
    click.echo("Our App's DB has been initialized!")


def get_db():
    """Method in charge of returning the DB instance of our Flask App.

    Returns
    -------
    Connection
        The connection to the app's DB.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


# =================================================================================================
# PRIVATE METHODS for DB interaction
# =================================================================================================


def __close_db(*args):
    """Private method in charge of closing the DB."""
    db = g.pop("db", None)

    if db is not None:
        db.close()


def __init_db():
    """Private method in charge of initializing the DB."""
    db = get_db()

    with current_app.open_resource("restdb/schema.sql") as f:
        db.executescript(f.read().decode("utf8"))
