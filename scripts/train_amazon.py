import os
import joblib
import pandas as pd
import numpy as np
from implicit.als import AlternatingLeastSquares
from scipy.sparse import csr_matrix
import time

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

def train_amazon():
    print("--- Iniciando Fase 2: Entrenamiento Modelo Amazon ---")
    
    # 1. Cargar Datos
    print("[1/3] Cargando matriz CSR y Piedra Rosetta...")
    train_matrix = joblib.load(os.path.join(PROCESSED_DIR, 'train_matrix.pkl'))
    mapeos = joblib.load(os.path.join(PROCESSED_DIR, 'mapeos_ids.pkl'))
    
    user_to_idx = mapeos['user_to_idx']
    item_to_idx = mapeos['item_to_idx']
    
    # 2. Entrenamiento
    print(f"[2/3] Entrenando ALS para {len(user_to_idx)} usuarios y {len(item_to_idx)} items...")
    model = AlternatingLeastSquares(
        factors=64, 
        regularization=0.05, 
        iterations=20, 
        calculate_training_loss=True,
        random_state=42
    )
    
    start_time = time.time()
    model.fit(train_matrix.tocsr())
    end_time = time.time()
    
    print(f"Entrenamiento completado en {end_time - start_time:.2f} segundos.")
    
    # 3. Persistencia
    print("[3/3] Guardando modelo...")
    joblib.dump(model, os.path.join(MODELS_DIR, 'amazon_model.pkl'))
    
    print("--- Fase 2 (Amazon) Completada Exitosamente ---")

if __name__ == "__main__":
    train_amazon()
