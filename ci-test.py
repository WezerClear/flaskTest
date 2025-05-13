import pytest
from unittest.mock import patch
from api import app



#pip-audit
#safety check
#bandit -r . --exit-zero

#pytest ci-test.py -v


@pytest.fixture
def client():
    """Fixture to provide a test client for the api."""
    with app.test_client() as client:
        yield client


# Test for rendering the login form
def test_view_form(client):
    """Test that the login form is rendered correctly."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Login Form" in response.data


# Test for handling GET request with valid credentials
def test_handle_get_valid_credentials(client):
    """Test the GET handler with valid credentials using a mocked ddb."""
    with patch("api.ddb", return_value=True):  # Mock ddb to always return True.
        response = client.get(
            "/handle_get",
            query_string={"username": "valid_user", "password": "valid_pass"},
        )
        assert response.status_code == 200
        assert b"Welcome!!!" in response.data


# Test for handling GET request with invalid credentials
def test_handle_get_invalid_credentials(client):
    """Test the GET handler with invalid credentials using a mocked ddb."""
    with patch("api.ddb", return_value=False):  # Mock ddb to always return False.
        response = client.get(
            "/handle_get",
            query_string={"username": "invalid_user", "password": "invalid_pass"},
        )
        assert response.status_code == 200
        assert b"invalid credentials!" in response.data


# Test for handling POST request with valid credentials
def test_handle_post_valid_credentials(client):
    """Test the POST handler with valid credentials using a mocked ddb."""
    with patch("api.ddb", return_value=True):  # Mock ddb to always return True.
        response = client.post(
            "/handle_post", data={"username": "valid_user", "password": "valid_pass"}
        )
        assert response.status_code == 200
        assert b"Welcome!!!" in response.data


# Test for handling POST request with invalid credentials
def test_handle_post_invalid_credentials(client):
    """Test the POST handler with invalid credentials using a mocked ddb."""
    with patch("api.ddb", return_value=False):  # Mock ddb to always return False.
        response = client.post(
            "/handle_post",
            data={"username": "'or 1=1--", "password": "invalid_pass"},
        )
        assert response.status_code == 200
        assert b"invalid credentials!" in response.data


'''# Test for the ddb function directly (mocked file reading)
def test_ddb_mocked_file_reading():
    """Test the ddb function by mocking file reading."""
    mock_users = {"user1": "pass1", "user2": "pass2"}

    # Mock the open function to simulate a file with mock_users data.
    with patch("builtins.open", create=True) as mock_open:
        mock_open.return_value.__enter__.return_value = iter(
            ["user1|pass1\n", "user2|pass2\n"]
        )
        from api import ddb

        assert ddb("user1", "pass1") is True
        assert ddb("user2", "wrongpass") is False
        assert ddb("unknown_user", "pass1") is False'''
