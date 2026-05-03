from fastapi.testclient import TestClient
from unittest.mock import patch
from api.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

@patch('api.routes.recommendations.recsys_service')
def test_recommend_endpoint(mock_service):
    # Mock service response
    mock_service.get_user_recommendations.return_value = {
        "user_id": "test_user",
        "recommendations": [{"asin": "A1", "title": "Title 1", "image": "url", "category": "cat"}]
    }
    
    response = client.get("/recommend/test_user")
    assert response.status_code == 200
    assert response.json()["user_id"] == "test_user"

@patch('api.routes.recommendations.recsys_service')
def test_similar_endpoint_not_found(mock_service):
    mock_service.get_similar_items.side_effect = ValueError("Item not found")
    
    response = client.get("/similar/invalid_item")
    assert response.status_code == 404
    assert "Item not found" in response.json()["detail"]
