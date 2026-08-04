from src import app as app_module


def test_root_redirect(client):
    # Arrange: client fixture
    # Act
    response = client.get("/", follow_redirects=False)
    # Assert
    assert response.status_code in (307, 308)
    assert response.headers.get("location") == "/static/index.html"


def test_get_activities(client):
    # Arrange
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_and_reflects_in_list(client):
    # Arrange
    activity = "Chess Club"
    email = "testuser@example.com"

    # Act - sign up
    response = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert "Signed up" in body.get("message", "")

    # Act - fetch activities to verify
    resp2 = client.get("/activities")
    assert resp2.status_code == 200
    assert email in resp2.json()[activity]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Programming Class"
    email = "duplicate@example.com"
    r1 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r1.status_code == 200

    # Act
    r2 = client.post(f"/activities/{activity}/signup", params={"email": email})

    # Assert
    assert r2.status_code == 400


def test_signup_unknown_activity_returns_404(client):
    # Arrange / Act
    response = client.post("/activities/NoSuchActivity/signup", params={"email": "a@b.com"})
    # Assert
    assert response.status_code == 404


def test_unregister_success(client):
    # Arrange
    activity = "Gym Class"
    email = "to_remove@example.com"
    r1 = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert r1.status_code == 200

    # Act - remove
    r2 = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert r2.status_code == 200
    r3 = client.get("/activities")
    assert email not in r3.json()[activity]["participants"]


def test_unregister_nonexistent_participant_returns_404(client):
    # Arrange / Act
    activity = "Swimming Club"
    email = "nonexistent@example.com"
    r = client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Assert
    assert r.status_code == 404


def test_unregister_unknown_activity_returns_404(client):
    # Act
    r = client.delete("/activities/NoActivity/participants", params={"email": "x@y.com"})
    # Assert
    assert r.status_code == 404
