import os
import joblib
import logging
from typing import Dict, Any
from core.config import settings

logger = logging.getLogger(__name__)

class ModelLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.model = None
        self.mapeos = None
        self.train_matrix = None
        self.asin_to_meta = None
        self.resources_loaded = False
        self.load_all()

    def load_all(self):
        try:
            logger.info("Loading models and mappings...")
            self.model = joblib.load(os.path.join(settings.MODELS_DIR, 'amazon_model.pkl'))
            self.mapeos = joblib.load(os.path.join(settings.PROCESSED_DIR, 'mapeos_ids.pkl'))
            self.train_matrix = joblib.load(os.path.join(settings.PROCESSED_DIR, 'train_matrix.pkl')).tocsr()
            
            try:
                self.asin_to_meta = joblib.load(os.path.join(settings.PROCESSED_DIR, 'asin_to_meta.pkl'))
            except Exception:
                self.asin_to_meta = {}
                logger.warning("Metadata file not found, using empty mapping.")
            
            self.resources_loaded = True
            logger.info("Resources loaded successfully.")
        except Exception as e:
            logger.error(f"Error loading resources: {e}")
            raise RuntimeError(f"Failed to load engine resources: {e}")

    def get_mappings(self) -> Dict[str, Any]:
        return self.mapeos

    def get_model(self) -> Any:
        return self.model

    def get_train_matrix(self) -> Any:
        return self.train_matrix

    def get_metadata(self) -> Dict[str, Any]:
        return self.asin_to_meta

model_loader = ModelLoader()
