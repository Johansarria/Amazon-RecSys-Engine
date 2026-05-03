from pydantic import BaseModel
from typing import List, Optional

class ItemDetail(BaseModel):
    asin: str
    title: str
    image: str
    category: str
    score: Optional[float] = None

class RecommendationResponse(BaseModel):
    user_id: str
    recommendations: List[ItemDetail]

class SimilarItemsResponse(BaseModel):
    asin_original: str
    similar_products: List[ItemDetail]
