from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_request_shorten_url():
    long_url = "http://some_big_long_url.com/"
    response = client.post("/urls", json={"url": long_url})
    assert response.status_code == 201, f"Wrong status code ({response.status_code})"
    resp_json = response.json()
    assert "url" in resp_json
    assert resp_json["url"] == long_url

def test_request_shorten_wrong_url():
    long_url = "file://some_big_long_url.com/"
    response = client.post("/urls", json={"url": long_url})
    assert response.status_code == 422

def test_request_shorten_url_and_get_original():
    long_url = "http://some_big_long_url.com/"
    response = client.post("/urls", json={"url": long_url})
    resp_json = response.json()

    resp_redirect = client.get(resp_json["short"], allow_redirects=False)
    assert resp_redirect.status_code == 301
    assert resp_redirect.headers["location"] == long_url
