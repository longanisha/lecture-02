from fastapi.testclient import TestClient
from main import app  # or whatever your app module is

client = TestClient(app)

def test_basic_division():
    r = client.post("/calculate", params={"expr": "30/4"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 7.5) < 1e-9

def test_percent_subtraction():
    r = client.post("/calculate", params={"expr": "100 - 6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 94.0) < 1e-9

def test_standalone_percent():
    r = client.post("/calculate", params={"expr": "6%"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is True
    assert abs(data["result"] - 0.06) < 1e-9

def test_invalid_expr_returns_ok_false():
    r = client.post("/calculate", params={"expr": "2**(3"})
    assert r.status_code == 200
    data = r.json()
    assert data["ok"] is False
    assert "error" in data and data["error"] != ""


# --- Tests for GET /history ---

def test_history_empty_initially():
    client.delete("/history")
    r = client.get("/history")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, list)
    assert len(data) == 0


def test_history_records_after_calculate():
    client.delete("/history")
    r1 = client.post("/calculate", params={"expr": "1+1"})
    assert r1.status_code == 200 and r1.json()["ok"] is True
    r = client.get("/history")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["expr"] == "1+1"
    assert abs(data[0]["result"] - 2) < 1e-9
    assert "time" in data[0]


def test_history_limit_and_order():
    client.delete("/history")
    client.post("/calculate", params={"expr": "1+1"})
    client.post("/calculate", params={"expr": "2+2"})
    client.post("/calculate", params={"expr": "3+3"})
    r = client.get("/history", params={"limit": 2})
    assert r.status_code == 200
    data = r.json()
    # Most recent first, and limited to 2
    assert len(data) == 2
    assert data[0]["expr"] == "3+3"
    assert data[1]["expr"] == "2+2"


# --- Tests for DELETE /history ---

def test_clear_history_makes_empty():
    client.delete("/history")
    client.post("/calculate", params={"expr": "5*5"})
    client.post("/calculate", params={"expr": "6*6"})
    r_before = client.get("/history")
    assert len(r_before.json()) == 2
    r = client.delete("/history")
    assert r.status_code == 200
    assert r.json().get("ok") is True
    r_after = client.get("/history")
    assert r_after.status_code == 200
    assert r_after.json() == []


def test_clear_history_idempotent():
    client.delete("/history")
    r1 = client.delete("/history")
    assert r1.status_code == 200 and r1.json().get("ok") is True
    r2 = client.get("/history")
    assert r2.status_code == 200 and r2.json() == []


def test_history_after_clear_then_calculate():
    client.delete("/history")
    client.post("/calculate", params={"expr": "10/2"})
    r = client.get("/history")
    assert r.status_code == 200
    data = r.json()
    assert len(data) == 1
    assert data[0]["expr"] == "10/2"


# TODO Add more tests