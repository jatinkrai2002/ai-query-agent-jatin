from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_query_pods():
    response = client.post("/query", json={"query": "How many pods are in the default namespace?"})
    assert response.status_code == 200
    assert "There are" in response.json()["answer"]

def test_query_unrecognized():
    response = client.post("/query", json={"query": "What is the meaning of life?"})
    assert response.status_code == 200
    assert response.json()["answer"] != "Query not recognized."

"""
Run your tests with:

pytest test_main.py


"""