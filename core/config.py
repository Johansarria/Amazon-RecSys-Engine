import os
from pydantic import BaseModel
from typing import List

class Settings(BaseModel):
    PROJECT_NAME: str = "Universal RecSys Engine"
    API_V1_STR: str = "/api/v1"
    
    # Paths
    # We use a factory or static calculation for paths
    BASE_DIR: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    MODELS_DIR: str = os.path.join(BASE_DIR, "models")
    PROCESSED_DIR: str = os.path.join(BASE_DIR, "processed")
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

settings = Settings()
