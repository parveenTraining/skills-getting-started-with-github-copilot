from urllib.parse import quote


def test_get_activities(client):
    # Arrange (client fixture)
    # Act
    resp = client.get("/activities")
    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_adds_participant(client):
    # Arrange
    name = "Basketball Team"
    email = "newstudent@example.com"
    # Act
    resp = client.post(f"/activities/{quote(name)}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 200
    get_resp = client.get("/activities")
    assert email in get_resp.json()[name]["participants"]


def test_signup_duplicate(client):
    # Arrange
    name = "Basketball Team"
    email = "dupstudent@example.com"
    # Act
    r1 = client.post(f"/activities/{quote(name)}/signup", params={"email": email})
    r2 = client.post(f"/activities/{quote(name)}/signup", params={"email": email})
    # Assert
    assert r1.status_code == 200
    assert r2.status_code == 400


def test_signup_invalid_activity(client):
    # Arrange
    name = "Nonexistent Club"
    email = "x@example.com"
    # Act
    resp = client.post(f"/activities/{quote(name)}/signup", params={"email": email})
    # Assert
    assert resp.status_code == 404


def test_remove_participant(client):
    # Arrange
    name = "Basketball Team"
    email = "alex@mergington.edu"
    # Pre-check: ensure participant exists
    assert email in client.get("/activities").json()[name]["participants"]
    # Act
    resp = client.delete(f"/activities/{quote(name)}/participants", params={"email": email})
    # Assert
    assert resp.status_code == 200
    assert email not in client.get("/activities").json()[name]["participants"]


def test_remove_nonexistent_participant(client):
    # Arrange
    name = "Basketball Team"
    email = "noone@example.com"
    # Act
    resp = client.delete(f"/activities/{quote(name)}/participants", params={"email": email})
    # Assert
    assert resp.status_code == 404
