# tests/test_app.py
import pytest
from app import app  # Import your Flask app instance

@pytest.fixture
def client():
    """
    Fixture to create a test client for the Flask app.  This will
    allow you to simulate making requests to your app without running
    a full server.
    """
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """
    Test the main index route ('/').  This function checks if the
    route returns a 200 status code (OK) and if a specific string
    is present in the response data.  Adjust the string to match
    something that is actually on your main page.
    """
    response = client.get('/')
    assert response.status_code == 200
    #  Important:  Change this string to something that you
    #  know will be on your main page.  This is a basic
    #  check to make sure the route is rendering something.
    assert b"<!DOCTYPE html>" in response.data

def test_download_csv_route(client):
    """
    Test the download CSV route ('/download'). This function checks
    if the route returns a 200 status code, the correct content type,
    and the expected filename in the Content-Disposition header.
    """
    response = client.get('/download')
    assert response.status_code == 200
    assert response.content_type == 'text/csv'
    assert response.headers['Content-Disposition'] == 'attachment; filename=filtered_energy_data.csv'

#  Add more test functions as you expand your testing.  For example:
#  - Test different routes
#  - Test form submissions
#  - Test database interactions
#  - Test error handling
