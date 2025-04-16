"""Tests for the Flask application."""
import pytest
from app import app  # Import your Flask app instance

@pytest.fixture
def test_client():
    """
    Fixture to create a test client for the Flask app.
    Allows simulating requests without running a full server.
    """
    with app.test_client() as client:
        yield client

def test_index_route(test_client):
    """
    Test the main index route ('/').
    Checks for a 200 status code and expected content.
    """
    response = test_client.get('/')
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data

def test_download_csv_route(test_client):
    """
    Test the download CSV route ('/download').
    Checks for 200 status, correct content type, and filename.
    """
    response = test_client.get('/download')
    assert response.status_code == 200
    assert response.content_type == 'text/csv'
    assert response.headers['Content-Disposition'] == (
        'attachment; filename=filtered_energy_data.csv'
    )
