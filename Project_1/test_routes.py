import pytest
from routes import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# static routes
def test_index_route(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<html" in response.data or b"<!DOCTYPE html" in response.data
    assert "text/html" in response.content_type

def test_map_route(client):
    response = client.get("/map")
    assert response.status_code == 200
    assert b"map" in response.data.lower()
    assert "text/html" in response.content_type

def test_about_route(client):
    response = client.get("/about")
    assert response.status_code == 200
    assert "text/html" in response.content_type

def test_contact_route(client):
    response = client.get("/contact")
    assert response.status_code == 200
    assert b"contact" in response.data.lower()
    assert "text/html" in response.content_type

def test_address_route(client):
    response = client.get("/address")
    assert response.status_code == 200
    assert "text/html" in response.content_type

def test_models_route(client):
    response = client.get("/models")
    assert response.status_code == 200
    assert "text/html" in response.content_type


# stops
def test_stops_route(client):
    response = client.get("/stops")
    assert response.status_code == 200
    assert "text/html" in response.content_type

def test_stops_route_content_type(client):
    response = client.get("/stops")
    assert response.content_type == "text/html; charset=utf-8"


# routes
def test_routes_with_valid_coordinates(client):
    response = client.get("/routes?lat=21.3&lng=-157.8")
    assert response.status_code == 200
    assert response.is_json
    assert isinstance(response.get_json(), list)

def test_routes_with_far_coordinates(client):
    response = client.get("/routes?lat=0&lng=0")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)
    assert len(response.get_json()) == 0  # expecting 0 results

def test_routes_with_missing_parameters(client):
    response = client.get("/routes")
    assert response.status_code == 500
    assert response.is_json
    assert "error" in response.get_json()


# arrivals
def test_arrivals_with_default_stop(client):
    response = client.get("/arrivals")
    assert response.status_code in [200, 500]  # allow for API error
    assert response.is_json

def test_arrivals_with_invalid_stop_id(client):
    response = client.get("/arrivals?stop_ID=invalid")
    assert response.status_code in [200, 500]
    assert response.is_json
