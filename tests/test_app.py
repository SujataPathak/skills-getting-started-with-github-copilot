from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert "Soccer" in data
    assert isinstance(data["Soccer"]["participants"], list)


def test_signup_duplicate_and_remove():
    activity = "Soccer"
    email = "testuser@example.com"

    # Ensure clean state
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Sign up
    r = client.post(f"/activities/{activity}/signup?email={email}")
    assert r.status_code == 200
    assert email in activities[activity]["participants"]

    # Duplicate signup should fail
    r2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert r2.status_code == 400

    # Remove participant
    r3 = client.delete(f"/activities/{activity}/participants?email={email}")
    assert r3.status_code == 200
    assert email not in activities[activity]["participants"]


def test_remove_errors():
    # Activity not found
    r = client.delete("/activities/NoSuchActivity/participants?email=someone@example.com")
    assert r.status_code == 404

    # Email not signed up
    r2 = client.delete("/activities/Soccer/participants?email=not@present.example")
    assert r2.status_code == 400
