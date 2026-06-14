from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_docs_exists():
    res = client.get("/docs")
    
    assert res.status_code == 200
    
    
def test_openapi_exists():
    res = client.get("/openapi.json")
    
    assert res.status_code == 200