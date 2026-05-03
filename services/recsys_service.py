import logging
from typing import List, Dict, Any
from infrastructure.model_loader import model_loader
from domain.schemas.recommendation import ItemDetail, RecommendationResponse, SimilarItemsResponse

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self):
        self.loader = model_loader
        self.mapeos = self.loader.get_mappings()
        self.model = self.loader.get_model()
        self.train_matrix = self.loader.get_train_matrix()
        self.asin_to_meta = self.loader.get_metadata()
        
        self.user_to_idx = self.mapeos['user_to_idx']
        self.idx_to_user = self.mapeos['idx_to_user']
        self.item_to_idx = self.mapeos['item_to_idx']
        self.idx_to_item = self.mapeos['idx_to_item']

    def get_user_recommendations(self, user_id: str, n: int = 5) -> RecommendationResponse:
        if user_id not in self.user_to_idx:
            raise ValueError(f"User {user_id} not found.")
        
        u_idx = self.user_to_idx[user_id]
        user_row = self.train_matrix[u_idx]
        
        ids, scores = self.model.recommend(u_idx, user_row, N=n)
        
        recommendations = []
        for i, score in zip(ids, scores):
            asin = self.idx_to_item[i]
            meta = self.asin_to_meta.get(asin, {})
            recommendations.append(ItemDetail(
                asin=asin,
                score=float(score),
                title=meta.get('title', asin),
                image=meta.get('image', 'https://via.placeholder.com/150'),
                category=meta.get('category', 'General')
            ))
            
        return RecommendationResponse(user_id=user_id, recommendations=recommendations)

    def get_similar_items(self, item_id: str, n: int = 5) -> SimilarItemsResponse:
        if item_id not in self.item_to_idx:
            raise ValueError(f"Item {item_id} not found.")
        
        i_idx = self.item_to_idx[item_id]
        ids, scores = self.model.similar_items(i_idx, N=n+1)
        
        similar = []
        for i, score in zip(ids[1:], scores[1:]):
            asin = self.idx_to_item[i]
            meta = self.asin_to_meta.get(asin, {})
            similar.append(ItemDetail(
                asin=asin,
                score=float(score),
                title=meta.get('title', asin),
                image=meta.get('image', 'https://via.placeholder.com/150'),
                category=meta.get('category', 'General')
            ))
            
        return SimilarItemsResponse(asin_original=item_id, similar_products=similar)

recsys_service = RecommendationService()
