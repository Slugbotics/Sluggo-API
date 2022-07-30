# get_database_configuration.py - method for getting database from env
# created by Isaac Trimble-Pederson
#
# Licensed under the Apache 2.0 License, see LICENSE for details.

import os


class DBConfigError(ValueError):
    pass


# Get database configuration from the environment
# Precondition: Environment variables must be loaded.
def get_database_configuration(BASE_DIR: str) -> dict:
    # valid engines below - note MariaDB maps to mysql as per Django docs
    valid_engines = ["sqlite3", "postgresql", "mysql", "oracle"]

    # Get engine, defaulting to sqlite3
    engine = os.environ.get("SLUGGO_DB_ENGINE")
    if engine is None:
        engine = "sqlite3"  # default to sqlite
    elif engine not in valid_engines:
        raise DBConfigError("Invalid engine selected!")

    # Create dictionary for database configuration with engine (which must
    # exist)
    db_dict = {"ENGINE": f"django.db.backends.{engine}"}

    # Configure NAME, defaulting for sqlite3 if not provided.
    DB_NAME = os.environ.get("SLUGGO_DB_NAME")
    if DB_NAME is None and engine == "sqlite3":
        DB_NAME = os.path.join(BASE_DIR, "db.sqlite3")

    # Get potential fields
    DB_USER = os.environ.get("SLUGGO_DB_USER")
    DB_PASS = os.environ.get("SLUGGO_DB_PASS")
    DB_HOST = os.environ.get("SLUGGO_DB_HOST")
    DB_PORT = os.environ.get("SLUGGO_DB_PORT")

    # Add any of these values to their appropriate key if they exist
    if DB_NAME is not None:
        db_dict["NAME"] = DB_NAME
    if DB_USER is not None:
        db_dict["USER"] = DB_USER
    if DB_PASS is not None:
        db_dict["PASS"] = DB_PASS
    if DB_HOST is not None:
        db_dict["HOST"] = DB_HOST
    if DB_PORT is not None:
        db_dict["PORT"] = DB_PORT

    return {"default": db_dict}
