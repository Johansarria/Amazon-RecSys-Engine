import os
import datetime

# Importamos las librerías, pero manejamos si no están instaladas
try:
    import firebase_admin
    from firebase_admin import credentials, firestore
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

class FirebaseAnalytics:
    """
    Servicio para loggear las interacciones y analíticas en Firestore.
    Permanecerá inactivo hasta que se inicialice el proyecto MCP y se agregue la clave.
    """
    def __init__(self):
        self.db = None
        self.active = False
        
        # Ruta esperada a la llave de servicio de Firebase
        key_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'serviceAccountKey.json')
        
        if FIREBASE_AVAILABLE and os.path.exists(key_path):
            try:
                cred = credentials.Certificate(key_path)
                firebase_admin.initialize_app(cred)
                self.db = firestore.client()
                self.active = True
                print("Firebase inicializado correctamente.")
            except Exception as e:
                print(f"Error inicializando Firebase: {e}")
        else:
            print("Firebase inactivo: Falta firebase-admin o serviceAccountKey.json")
            
    def log_recommendation(self, user_id, recommendations, response_time_ms):
        """
        Guarda un registro de la recomendación entregada al usuario.
        """
        if not self.active:
            return False
            
        try:
            doc_ref = self.db.collection('recommendation_logs').document()
            doc_ref.set({
                'user_id': user_id,
                'timestamp': datetime.datetime.now(datetime.timezone.utc),
                'recommended_asins': [r['asin'] for r in recommendations],
                'response_time_ms': response_time_ms
            })
            return True
        except Exception as e:
            print(f"Error logueando en Firebase: {e}")
            return False

# Instancia singleton para exportar
analytics = FirebaseAnalytics()
