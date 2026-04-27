import os
import joblib
import pandas as pd
import numpy as np
from lightfm import LightFM
from lightfm.evaluation import precision_at_k, auc_score
from scipy.sparse import csr_matrix
import time

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

def train_hybrid():
    print("--- Iniciando Fase 2.5: Entrenamiento Modelo Híbrido (LightFM) ---")
    
    # 1. Cargar Datos
    print("[1/4] Cargando matrices e item features...")
    train_matrix = joblib.load(os.path.join(PROCESSED_DIR, 'train_matrix.pkl'))
    item_features = joblib.load(os.path.join(PROCESSED_DIR, 'item_features.pkl'))
    
    # 2. Configuración y Entrenamiento
    print("[2/4] Configurando y entrenando modelo LightFM (WARP loss)...")
    # WARP (Weighted Approximate-Rank Pairwise) es ideal para optimizar el top de la lista
    model = LightFM(
        no_components=64, 
        loss='warp', 
        learning_rate=0.05, 
        random_state=42
    )
    
    start_time = time.time()
    # Entrenamos usando item_features para que el modelo aprenda la relación con categorías
    model.fit(
        train_matrix, 
        item_features=item_features, 
        epochs=30, 
        num_threads=4
    )
    end_time = time.time()
    
    print(f"Entrenamiento híbrido completado en {end_time - start_time:.2f} segundos.")
    
    # 3. Evaluación
    print("[3/4] Evaluando modelo...")
    test_df = pd.read_csv(os.path.join(PROCESSED_DIR, 'test_interactions.csv'))
    n_users, n_items = train_matrix.shape
    test_matrix = csr_matrix(
        (test_df['event_weight'], (test_df['user_idx'], test_df['item_idx'])),
        shape=(n_users, n_items)
    )
    
    # Usamos Precision@10 y AUC como métricas estándar de LightFM
    train_precision = precision_at_k(model, train_matrix, item_features=item_features, k=10).mean()
    test_precision = precision_at_k(model, test_matrix, item_features=item_features, k=10).mean()
    
    print(f"Precision@10 (Train): {train_precision:.4f}")
    print(f"Precision@10 (Test): {test_precision:.4f}")
    
    # 4. Persistencia
    print("[4/4] Guardando modelo híbrido...")
    joblib.dump(model, os.path.join(MODELS_DIR, 'hybrid_model.pkl'))
    
    print("--- Fase 2.5 Completada Exitosamente ---")

if __name__ == "__main__":
    train_hybrid()
