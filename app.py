import streamlit as st
import requests
import joblib
import os

# Configuración de página
st.set_page_config(page_title="Amazon RecSys", page_icon="📚", layout="wide")

# Rutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_DIR = os.path.join(BASE_DIR, 'processed')

# Cargar metadatos localmente para el frontend
@st.cache_data
def load_metadata():
    try:
        return joblib.load(os.path.join(PROCESSED_DIR, 'asin_to_meta.pkl'))
    except:
        return {}

asin_to_meta = load_metadata()

# URL de la API (Asegúrate de que la API esté corriendo en WSL o localmente)
API_URL = "http://localhost:8000"

st.title("📚 Amazon Magazine Recommender")
st.markdown("Sistema de Recomendación basado en Filtrado Colaborativo (ALS) y FastAPI.")

# Sidebar para controles
with st.sidebar:
    st.header("Configuración")
    user_id = st.text_input("Ingresa un Reviewer ID:", "A19FKU6JZQ2ECJ")
    n_recs = st.slider("Cantidad de recomendaciones:", 1, 10, 5)
    
    if st.button("Obtener Recomendaciones"):
        get_recs = True
    else:
        get_recs = False

# Área principal
if get_recs and user_id:
    with st.spinner("Consultando al motor de recomendaciones..."):
        try:
            # Llamada a la API
            response = requests.get(f"{API_URL}/recommend/{user_id}?n={n_recs}")
            
            if response.status_code == 200:
                data = response.json()
                recs = data.get("recommendations", [])
                
                st.success(f"¡Recomendaciones generadas para el usuario **{user_id}**!")
                
                # Mostrar en formato grid (columnas)
                cols = st.columns(len(recs))
                
                for i, rec in enumerate(recs):
                    asin = rec['asin']
                    score = rec['score']
                    meta = asin_to_meta.get(asin, {'title': asin, 'image': 'https://via.placeholder.com/150', 'category': 'Desconocida'})
                    
                    with cols[i]:
                        st.image(meta['image'], use_column_width=True)
                        st.markdown(f"**{meta['title']}**")
                        st.caption(f"Categoría: {meta['category']}")
                        st.info(f"Score: {score:.3f}")
                        
            elif response.status_code == 404:
                st.warning("Usuario no encontrado en la base de datos (Cold Start no manejado aún).")
            else:
                st.error(f"Error de la API: {response.text}")
                
        except requests.exceptions.ConnectionError:
            st.error("No se pudo conectar a la API. Asegúrate de que FastAPI esté corriendo (uvicorn api.main:app).")

st.markdown("---")
st.markdown("*Olist & Amazon RecSys Engine - Arquitectura de Portafolio*")
