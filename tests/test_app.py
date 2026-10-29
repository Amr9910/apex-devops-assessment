from unittest.mock import MagicMock

import app as app_module

client = app_module.app.test_client()

def test_root_returns_service_name():
    response = client.get("/")
    assert response.status_code == 200
    assert response.get_json()["service"] == "Apex Operations API"

def test_root_includes_version():
    response = client.get("/")
    assert "version" in response.get_json()

def test_health_is_successful():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"

def test_metrics_has_uptime_metric():
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "apex_api_uptime_seconds" in response.get_data(as_text=True)

def test_ready_when_database_works(monkeypatch):
    fake_conn = MagicMock()
    fake_cursor = MagicMock()
    fake_conn.cursor.return_value.__enter__.return_value = fake_cursor
    monkeypatch.setattr(app_module, "database_connection", lambda: fake_conn)
    response = client.get("/ready")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ready"

def test_ready_when_database_is_down(monkeypatch):
    def raise_connection_error():
        raise OSError("simulated database outage")
    monkeypatch.setattr(app_module, "database_connection", raise_connection_error)
    response = client.get("/ready")
    assert response.status_code == 503
    assert response.get_json()["status"] == "not_ready"
