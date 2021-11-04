import pytest
from main import connection

@pytest.fixture
def db_connection():
    return connection()

