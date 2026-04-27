import os
import joblib
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')

def test_recommendations():
    print("--- Probando Recomendaciones ---")
    model = joblib.load(os.path.join(MODELS_DIR, 'als_model.pkl'))
    user_to_idx = joblib.load(os.path.join(PROCESSED_DIR, 'user_to_idx.pkl'))
    idx_to_item = joblib.load(os.path.join(PROCESSED_DIR, 'idx_to_item.pkl'))
    train_matrix = joblib.load(os.path.join(PROCESSED_DIR, 'train_matrix.pkl'))
    
    # Tomar un usuario que tenga interacciones
    test_user_idx = 100
    print(f"Usuario de prueba (ID Interno): {test_user_idx}")
    
    # Generar recomendaciones
    ids, scores = model.recommend(test_user_idx, train_matrix[test_user_idx], N=5)
    
    print("\nTop 5 Recomendaciones:")
    for i, (item_idx, score) in enumerate(zip(ids, scores)):
        item_id = idx_to_item[item_idx]
        print(f"{i+1}. Item ID: {item_id} (Score: {score:.4f})")

if __name__ == "__main__":
    test_recommendations()
