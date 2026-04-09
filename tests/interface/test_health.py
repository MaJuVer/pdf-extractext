"""
Tests para endpoints de health check.

Verifican que los endpoints de monitoreo funcionen correctamente.
"""

from fastapi.testclient import TestClient

from src.interface.main import app

client = TestClient(app)


def test_health_check_returns_healthy():
    """Health check debe retornar estado healthy."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "version" in data


def test_readiness_check_returns_ready():
    """Readiness check debe retornar estado ready."""
    response = client.get("/health/ready")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ready"
    assert "timestamp" in data
    assert "version" in data
