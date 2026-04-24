import io
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from src.main.http.endpoints import app, baseEndpoint, usersEndpoint, workoutsEndpoint, \
    exerciseSetsEndpoint, accelDataEndpoint, gyroDataEndpoint

client = TestClient(app)


@pytest.fixture(autouse=True)
def mock_db():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    with patch("src.main.http.endpointsLogic.getDbConnection", return_value=mock_conn):
        yield mock_cursor


def testPing():
    response = client.get(baseEndpoint)
    assert response.status_code == 200
    assert response.json() == {"Ping": "Pong"}


def testAddUser(mock_db):
    payload = {"userID": "u1", "email": "test@example.com", "name": "Test User"}
    response = client.post(usersEndpoint, json=payload)
    assert response.status_code == 200
    assert response.json() == payload
    mock_db.execute.assert_called_once()


def testAddWorkout(mock_db):
    payload = {"workoutID": "w1", "userID": "u1", "time": "2026-04-24T10:00:00"}
    response = client.post(workoutsEndpoint, json=payload)
    assert response.status_code == 200
    assert response.json()["workoutID"] == payload["workoutID"]
    mock_db.execute.assert_called_once()


def testAddExerciseSet(mock_db):
    payload = {
        "exerciseSetID": "es1",
        "workoutID": "w1",
        "userID": "u1",
        "exercise": "squat",
        "reps": 10,
    }
    response = client.post(exerciseSetsEndpoint, json=payload)
    assert response.status_code == 200
    assert response.json() == payload
    mock_db.execute.assert_called_once()


def _csv_bytes():
    rows = [
        "1.0,2.0,3.0,es1,w1,u1",
        "4.0,5.0,6.0,es1,w1,u1",
        "7.0,8.0,9.0,es1,w1,u1",
    ]
    return io.BytesIO("\n".join(rows).encode())


def testAddAccelData(mock_db):
    response = client.post(
        accelDataEndpoint,
        files={"acceleration_data": ("accel.csv", _csv_bytes(), "text/csv")},
    )
    assert response.status_code == 200
    assert response.json()["numRows"] == 3
    assert mock_db.execute.call_count >= 1


def testAddGyroData(mock_db):
    response = client.post(
        gyroDataEndpoint,
        files={"gyroscope_data": ("gyro.csv", _csv_bytes(), "text/csv")},
    )
    assert response.status_code == 200
    assert response.json()["numRows"] == 3
    assert mock_db.execute.call_count >= 1
