import pytest
from unittest.mock import MagicMock
import numpy as np
from scipy.sparse import csr_matrix

@pytest.fixture
def mock_model():
    model = MagicMock()
    # Mock recommend method - using indices that exist in mappings (0, 1, 2)
    model.recommend.return_value = (np.array([0, 1, 2]), np.array([0.9, 0.8, 0.7]))
    # Mock similar_items method
    model.similar_items.return_value = (np.array([0, 1, 2]), np.array([0.95, 0.85, 0.75]))
    return model

@pytest.fixture
def mock_mappings():
    return {
        'user_to_idx': {'user1': 0, 'user2': 1},
        'idx_to_user': {0: 'user1', 1: 'user2'},
        'item_to_idx': {'item1': 0, 'item2': 1, 'item3': 2},
        'idx_to_item': {0: 'item1', 1: 'item2', 2: 'item3'}
    }

@pytest.fixture
def mock_train_matrix():
    return csr_matrix(np.random.rand(2, 3))

@pytest.fixture
def mock_metadata():
    return {
        'item1': {'title': 'Item 1', 'image': 'img1', 'category': 'Cat1'},
        'item2': {'title': 'Item 2', 'image': 'img2', 'category': 'Cat2'},
        'item3': {'title': 'Item 3', 'image': 'img3', 'category': 'Cat3'}
    }
