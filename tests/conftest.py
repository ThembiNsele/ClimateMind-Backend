import pytest
import pickle
from unittest.mock import patch
# Importing climatemind module immediately runs the code that generates a Flask app object

import app

# Setup local SQLITE database
# Deosn't work right now.
def setup_local_sqlite():
    sqlite_path = 'sqlite:////tmp/temp.db'
    sqlalchemy_uri_patch = patch.object(app.DevelopmentConfig, 'SQLALCHEMY_DATABASE_URI', sqlite_path)
    mssql_unique_id_patch = patch.object(app.models, 'UNIQUEIDENTIFIER', app.db.Integer())

    with sqlalchemy_uri_patch:
        with mssql_unique_id_patch:
            import climatemind
        assert climatemind.app.config['SQLALCHEMY_DATABASE_URI'] == sqlite_path
        climatemind.app.config["TESTING"] = True

        # Create tables if they don't exist
        with climatemind.app.app_context(), mssql_unique_id_patch:
            app.db.create_all()

        us = app.models.Sessions()
        us.postal_code = "43953"
        us.ip_address = "34235423513513513"
        with climatemind.app.app_context():
            app.db.session.add(us)
        app.db.session.commit()

@pytest.fixture
def networkx_ontology():
    ONTOLOGY_PATH = "output/Climate_Mind_DiGraph.gpickle"
    return pickle.load(open(ONTOLOGY_PATH, "rb"))


# Yields the client object. When requesting client as the fixture, then the test is automatically in the app context
@pytest.fixture
def client():
    with patch.object(app.DevelopmentConfig, 'SQLALCHEMY_DATABASE_URI', 'sqlite:////tmp/test.db'):
        import climatemind
        assert climatemind.app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:////tmp/test.db'
        climatemind.app.config["TESTING"] = True

        with climatemind.app.test_client() as client:
            yield client

