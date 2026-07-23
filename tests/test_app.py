from fastapi.testclient import TestClient

from src.app import app, activities


client = TestClient(app)


def test_duplicate_signup_is_rejected():
    original = activities["Chess Club"]["participants"][:]
    try:
        response = client.post("/activities/Chess%20Club/signup?email=student@mergington.edu")
        assert response.status_code == 200

        duplicate_response = client.post(
            "/activities/Chess%20Club/signup?email=student@mergington.edu"
        )

        assert duplicate_response.status_code == 400
        assert duplicate_response.json()["detail"] == "Student is already signed up for this activity"
        assert activities["Chess Club"]["participants"].count("student@mergington.edu") == 1
    finally:
        activities["Chess Club"]["participants"] = original


def test_unregister_participant_from_activity():
    original = activities["Chess Club"]["participants"][:]
    try:
        activities["Chess Club"]["participants"].append("remove-me@mergington.edu")

        response = client.delete(
            "/activities/Chess%20Club/signup?email=remove-me@mergington.edu"
        )

        assert response.status_code == 200
        assert response.json()["detail"] == "Removed remove-me@mergington.edu from Chess Club"
        assert "remove-me@mergington.edu" not in activities["Chess Club"]["participants"]
    finally:
        activities["Chess Club"]["participants"] = original
