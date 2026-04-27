from fastapi import FastAPI, HTTPException
import joblib
import os
import numpy as np
from scipy.sparse import csr_matrix

# Configuración de rutas
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, 'models')
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Amazon RecSys Engine API")

# Habilitar CORS para el frontend (Vite por defecto en 5173 o Streamlit en 8501)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción cambiar a dominios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Carga de recursos (Singleton)
print("Cargando modelo y mapeos...")
try:
    model = joblib.load(os.path.join(MODELS_DIR, 'amazon_model.pkl'))
    mapeos = joblib.load(os.path.join(PROCESSED_DIR, 'mapeos_ids.pkl'))
    # Cargamos la matriz de entrenamiento para el filtrado de recomendaciones
    train_matrix = joblib.load(os.path.join(PROCESSED_DIR, 'train_matrix.pkl')).tocsr()
    
    # Cargar metadatos para el frontend
    try:
        asin_to_meta = joblib.load(os.path.join(PROCESSED_DIR, 'asin_to_meta.pkl'))
    except:
        asin_to_meta = {}
    
    user_to_idx = mapeos['user_to_idx']
    idx_to_user = mapeos['idx_to_user']
    item_to_idx = mapeos['item_to_idx']
    idx_to_item = mapeos['idx_to_item']
    print("Recursos cargados exitosamente.")
except Exception as e:
    print(f"Error cargando recursos: {e}")

@app.get("/")
def read_root():
    return {"status": "online", "message": "Amazon Recommendation System API"}

@app.get("/recommend/{user_id}")
def get_recommendations(user_id: str, n: int = 5):
    """
    Devuelve las top N recomendaciones para un reviewerID de Amazon.
    """
    if user_id not in user_to_idx:
        raise HTTPException(status_code=404, detail="Usuario no encontrado en la base de datos.")
    
    u_idx = user_to_idx[user_id]
    
    try:
        # En implicit 0.7+, si pasamos un solo ID de usuario, 
        # debemos pasar la fila correspondiente de la matriz para el filtrado.
        user_row = train_matrix[u_idx]
        ids, scores = model.recommend(u_idx, user_row, N=n)
        
        recommendations = []
        for i, score in zip(ids, scores):
            asin = idx_to_item[i]
            meta = asin_to_meta.get(asin, {'title': asin, 'image': 'https://via.placeholder.com/150', 'category': 'General'})
            recommendations.append({
                "asin": asin,
                "score": float(score),
                "title": meta.get('title', asin),
                "image": meta.get('image', 'https://via.placeholder.com/150'),
                "category": meta.get('category', 'General')
            })
        
        return {
            "user_id": user_id,
            "recommendations": recommendations
        }
    except Exception as e:
        print(f"ERROR en recommend: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error en el modelo: {str(e)}")

@app.get("/similar/{item_id}")
def get_similar_items(item_id: str, n: int = 5):
    """
    Devuelve los top N productos similares a un ASIN dado.
    """
    if item_id not in item_to_idx:
        raise HTTPException(status_code=404, detail="Producto (ASIN) no encontrado.")
    
    i_idx = item_to_idx[item_id]
    
    try:
        # similar_items devuelve (item_ids, scores)
        ids, scores = model.similar_items(i_idx, N=n+1) # +1 porque el primero suele ser el mismo item
        
        similar = []
        for i, score in zip(ids[1:], scores[1:]): # Saltamos el primero
            similar.append({
                "asin": idx_to_item[i],
                "score": float(score)
            })
            
        return {
            "asin_original": item_id,
            "similar_products": similar
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al buscar similares: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
