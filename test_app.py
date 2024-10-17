import pytest
from app import app, get_current_season
from flask.testing import FlaskClient

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_redirect(client: FlaskClient):
    """Test that the home route redirects to the current-season route."""
    response = client.get('/')
    assert response.status_code == 302
    assert '/current-season' in response.location

def test_get_current_season():
    """Test the get_current_season function for accuracy."""
    assert get_current_season() == 'fall'

def test_current_season_anime(client: FlaskClient):
    """Test the current-season route."""
    response = client.get('/current-season')
    assert response.status_code == 200
