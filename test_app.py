import pytest
from app import app, fetch_and_store_fact, get_latest_fact

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


#Test 1 - Test that homepage loads
def test_homepage_loads(client):
    response = client.get("/")

    assert response.status_code == 200
    assert b"Fun Fact of the Day" in response.data

#Test 2 — Test that the new fact route works
def test_new_fact_route(client):
    response = client.get("/new-fact")

    # Should redirect or render page
    assert response.status_code in [200, 302]

#Test 3 - Test that the function that fetches the facts is working
def test_fetch_fact():
    fact = fetch_and_store_fact()

    assert fact is not None
    assert "text" in fact

#Test 4 - Checks that latest fact exists
def test_get_latest_fact():
    fetch_and_store_fact()

    fact = get_latest_fact()

    assert fact is not None
    assert "text" in fact

#Test 5 - Health check
def test_health_endpoint(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert b"ok" in response.data