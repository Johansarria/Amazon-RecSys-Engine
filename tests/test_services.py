import pytest
from unittest.mock import patch, MagicMock
from services.recsys_service import RecommendationService

def test_get_user_recommendations(mock_model, mock_mappings, mock_train_matrix, mock_metadata):
    # Mock ModelLoader before instantiating RecommendationService
    with patch('services.recsys_service.model_loader') as mock_loader:
        mock_loader.get_model.return_value = mock_model
        mock_loader.get_mappings.return_value = mock_mappings
        mock_loader.get_train_matrix.return_value = mock_train_matrix
        mock_loader.get_metadata.return_value = mock_metadata
        
        service = RecommendationService()
        response = service.get_user_recommendations("user1", n=3)
        
        assert response.user_id == "user1"
        assert len(response.recommendations) == 3
        # Check if model.recommend was called with correct user index
        mock_model.recommend.assert_called_once()

def test_get_user_recommendations_not_found(mock_model, mock_mappings, mock_train_matrix, mock_metadata):
    with patch('services.recsys_service.model_loader') as mock_loader:
        mock_loader.get_mappings.return_value = mock_mappings
        service = RecommendationService()
        
        with pytest.raises(ValueError, match="User unknown not found"):
            service.get_user_recommendations("unknown")

def test_get_similar_items(mock_model, mock_mappings, mock_train_matrix, mock_metadata):
    with patch('services.recsys_service.model_loader') as mock_loader:
        mock_loader.get_model.return_value = mock_model
        mock_loader.get_mappings.return_value = mock_mappings
        mock_loader.get_train_matrix.return_value = mock_train_matrix
        mock_loader.get_metadata.return_value = mock_metadata
        
        service = RecommendationService()
        response = service.get_similar_items("item1", n=2)
        
        assert response.asin_original == "item1"
        assert len(response.similar_products) == 2 # model.similar_items returns 3, we take 2 (N=n+1 skip 1)
