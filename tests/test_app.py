import sys
from pathlib import Path

from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import app

client = TestClient(app.app)


def test_unregister_participant_removes_student_from_activity():
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants?email={email}")

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in app.activities[activity_name]["participants"]

    app.activities[activity_name]["participants"].append(email)


def test_signup_for_activity_updates_participant_list_without_reload():
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    if email in app.activities[activity_name]["participants"]:
        app.activities[activity_name]["participants"].remove(email)

    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    assert response.status_code == 200
    assert email in app.activities[activity_name]["participants"]

    app.activities[activity_name]["participants"].remove(email)


def test_unregister_participant_rejects_unknown_student():
    response = client.delete("/activities/Chess Club/participants?email=unknown@mergington.edu")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is not registered for this activity"
