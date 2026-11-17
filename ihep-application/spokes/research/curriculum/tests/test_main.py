import pytest
from fastapi import Query

from app.core.exceptions import IHEPException
from app.main import app


@app.get("/__test__/validated")
async def _validated(n: int = Query(...)):
    return {"n": n}


@app.get("/__test__/ihep-error")
async def _ihep_error():
    raise IHEPException("Module not found", status_code=404, error_code="NOT_FOUND", detail={"id": 7})


@pytest.mark.api
def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "healthy", "environment": "development", "version": "1.0.0"}
    assert "x-process-time" in r.headers


@pytest.mark.api
def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["docs"] == "/api/docs"


@pytest.mark.api
def test_validation_error_handler_returns_422(client):
    r = client.get("/__test__/validated", params={"n": "not-a-number"})
    assert r.status_code == 422
    body = r.json()
    assert body["error"] == "VALIDATION_ERROR"
    assert body["message"] == "Request validation failed"
    assert body["detail"][0]["loc"] == ["query", "n"]


@pytest.mark.api
def test_ihep_exception_handler(client):
    r = client.get("/__test__/ihep-error")
    assert r.status_code == 404
    assert r.json() == {"error": "NOT_FOUND", "message": "Module not found", "detail": {"id": 7}}


@pytest.mark.api
def test_cors_preflight_allows_configured_origin(client):
    r = client.options(
        "/health",
        headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET"},
    )
    assert r.headers.get("access-control-allow-origin") == "http://localhost:3000"
