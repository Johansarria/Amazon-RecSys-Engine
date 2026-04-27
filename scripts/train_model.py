import os
import joblib
import pandas as pd
import numpy as np
from implicit.als import AlternatingLeastSquares
from implicit.evaluation import ndcg_at_k, train_test_split
from scipy.sparse import csr_matrix
import time

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')
MODELS_DIR = os.path.join(BASE_DIR, 'models')

if not os.path.exists(MODELS_DIR):
    os.makedirs(MODELS_DIR)

def train_model():
    print("--- Iniciando Fase 2: Entrenamiento del Modelo ---")
    
    # 1. Cargar Datos
    print("[1/4] Cargando matriz de entrenamiento...")
    train_matrix = joblib.load(os.path.join(PROCESSED_DIR, 'train_matrix.pkl'))
    
    # 2. Configuración y Entrenamiento
    print("[2/4] Configurando y entrenando modelo ALS...")
    # Hiperparámetros base recomendados para este volumen de datos
    model = AlternatingLeastSquares(
        factors=64, 
        regularization=0.05, 
        iterations=20, 
        calculate_training_loss=True,
        random_state=42
    )
    
    start_time = time.time()
    # En implicit 0.7.2+, fit espera la matriz (usuarios, items) por defecto
    model.fit(train_matrix.tocsr())
    end_time = time.time()
    
    print(f"Entrenamiento completado en {end_time - start_time:.2f} segundos.")
    
    # 3. Evaluación (Simplificada con NDCG@10)
    print("[3/4] Evaluando modelo...")
    # Cargamos el test set para evaluación
    test_df = pd.read_csv(os.path.join(PROCESSED_DIR, 'test_interactions.csv'))
    
    # Para evaluar en implicit necesitamos una matriz de test en el mismo formato
    n_users, n_items = train_matrix.shape
    test_matrix = csr_matrix(
        (test_df['event_weight'], (test_df['user_idx'], test_df['item_idx'])),
        shape=(n_users, n_items)
    )
    
    # Calculamos NDCG@10
    # Nota: implicit.evaluation.ndcg_at_k requiere la matriz de entrenamiento y la de test
    ndcg = ndcg_at_k(model, train_matrix.tocsr(), test_matrix.tocsr(), K=10)
    print(f"Métrica NDCG@10: {ndcg:.4f}")
    
    # 4. Persistencia
    print("[4/4] Guardando modelo...")
    joblib.dump(model, os.path.join(MODELS_DIR, 'als_model.pkl'))
    
    print("--- Fase 2 Completada Exitosamente ---")

if __name__ == "__main__":
    # Configurar variable de entorno para evitar advertencias de OpenBLAS/MKL si es necesario
    os.environ['OPENBLAS_NUM_THREADS'] = '1'
    train_model()
