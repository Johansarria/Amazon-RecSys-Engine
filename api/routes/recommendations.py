from fastapi import APIRouter, HTTPException, Query
from services.recsys_service import recsys_service
from domain.schemas.recommendation import RecommendationResponse, SimilarItemsResponse

router = APIRouter()

@router.get("/recommend/{user_id}", response_model=RecommendationResponse)
def get_recommendations(user_id: str, n: int = Query(5, ge=1, le=50)):
    """
    Devuelve las top N recomendaciones para un reviewerID de Amazon.
    """
    try:
        return recsys_service.get_user_recommendations(user_id, n)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal model error: {str(e)}")

@router.get("/similar/{item_id}", response_model=SimilarItemsResponse)
def get_similar_items(item_id: str, n: int = Query(5, ge=1, le=50)):
    """
    Devuelve los top N productos similares a un ASIN dado.
    """
    try:
        return recsys_service.get_similar_items(item_id, n)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error seeking similar items: {str(e)}")
