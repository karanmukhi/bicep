from google.cloud import bigquery
from fastapi.testclient import TestClient

from src.main.http.endpoints import *
from src.main.model.model import *

fastApiClient = TestClient(app)


def testPing():
    response = fastApiClient.get(baseEndpoint)
    assert response.status_code == 200
    assert response.json() == {"Ping": "Pong"}
