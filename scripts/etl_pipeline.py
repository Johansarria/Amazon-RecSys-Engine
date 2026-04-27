import pandas as pd
import numpy as np
import os
import json
from scipy.sparse import csr_matrix
import joblib

# Configuración de rutas (Compatibles con Windows y WSL)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'Dataset')
OUTPUT_DIR = os.path.join(BASE_DIR, 'processed')

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

class UniversalETL:
    def __init__(self, dataset_type='amazon'):
        self.dataset_type = dataset_type
        
    def _save_artifacts(self, train_matrix, user_to_idx, idx_to_user, item_to_idx, idx_to_item, test_df=None):
        print(f"[{self.dataset_type.upper()}] Guardando matriz CSR...")
        joblib.dump(train_matrix, os.path.join(OUTPUT_DIR, 'train_matrix.pkl'))
        
        print(f"[{self.dataset_type.upper()}] Guardando Piedra Rosetta (mapeos_ids.pkl)...")
        mapeos = {
            'user_to_idx': user_to_idx,
            'idx_to_user': idx_to_user,
            'item_to_idx': item_to_idx,
            'idx_to_item': idx_to_item
        }
        joblib.dump(mapeos, os.path.join(OUTPUT_DIR, 'mapeos_ids.pkl'))
        
        if test_df is not None:
            test_df.to_csv(os.path.join(OUTPUT_DIR, 'test_interactions.csv'), index=False)
            
        print("--- Fase 1 (ETL) Completada Exitosamente ---")
        print(f"Usuarios: {len(user_to_idx)}, Productos: {len(item_to_idx)}")
        print(f"Interacciones Entrenamiento: {train_matrix.nnz}")

    # ==========================================
    # 1. PARSER STREAMING (Prevención OOM - JSON)
    # ==========================================
    def parse_streaming(self, path):
        """Lee un archivo JSON grande línea por línea (yield). O(1) en RAM."""
        import gzip
        
        # Soporta tanto .json como .json.gz
        open_func = gzip.open if path.endswith('.gz') else open
        mode = 'rt' if path.endswith('.gz') else 'r'
        
        with open_func(path, mode, encoding='utf-8') as f:
            for line in f:
                yield json.loads(line)

    def run_amazon_streaming(self, json_filename):
        print(f"--- Iniciando ETL Streaming para {json_filename} ---")
        path = os.path.join(DATA_DIR, json_filename)
        
        # Usaremos diccionarios para el mapeo dinámico
        user_to_idx = {}
        item_to_idx = {}
        
        user_indices = []
        item_indices = []
        weights = []
        
        user_counter = 0
        item_counter = 0
        
        print("[1/3] Procesando JSON en streaming (yield)...")
        for data in self.parse_streaming(path):
            reviewer_id = data.get('reviewerID')
            asin = data.get('asin')
            overall = data.get('overall', 1.0) # Calificación
            
            if not reviewer_id or not asin:
                continue
                
            # Mapeo O(1) de Strings Gigantes a Enteros Ligeros
            if reviewer_id not in user_to_idx:
                user_to_idx[reviewer_id] = user_counter
                user_counter += 1
                
            if asin not in item_to_idx:
                item_to_idx[asin] = item_counter
                item_counter += 1
                
            user_indices.append(user_to_idx[reviewer_id])
            item_indices.append(item_to_idx[asin])
            weights.append(float(overall))
            
        print(f"[2/3] Generando diccionarios inversos (Piedra Rosetta)...")
        idx_to_user = {v: k for k, v in user_to_idx.items()}
        idx_to_item = {v: k for k, v in item_to_idx.items()}
        
        print(f"[3/3] Construyendo Matriz Dispersa CSR...")
        train_matrix = csr_matrix((weights, (user_indices, item_indices)), 
                                  shape=(user_counter, item_counter))
        
        self._save_artifacts(train_matrix, user_to_idx, idx_to_user, item_to_idx, idx_to_item)

    # ==========================================
    # 2. PARSER EN MEMORIA (Pandas - CSV Clásico)
    # ==========================================
    def run_olist_batch(self):
        print("--- Iniciando ETL en Memoria (Pandas) para Olist ---")
        
        # (Lógica original de Olist aquí, simplificada)
        orders = pd.read_csv(os.path.join(DATA_DIR, 'olist_orders_dataset.csv'), usecols=['order_id', 'customer_id', 'order_status', 'order_purchase_timestamp'])
        order_items = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_items_dataset.csv'), usecols=['order_id', 'product_id'])
        customers = pd.read_csv(os.path.join(DATA_DIR, 'olist_customers_dataset.csv'), usecols=['customer_id', 'customer_unique_id'])
        reviews = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_reviews_dataset.csv'), usecols=['order_id', 'review_score'])
        
        orders = orders[orders['order_status'] != 'canceled']
        df = pd.merge(orders, customers, on='customer_id')
        df = pd.merge(df, order_items, on='order_id')
        df = pd.merge(df, reviews, on='order_id', how='left')
        
        df['event_weight'] = 5
        df.loc[df['review_score'] == 5, 'event_weight'] += 5
        
        user_counts = df.groupby('customer_unique_id').size()
        recurrent_users = user_counts[user_counts >= 2].index
        df = df[df['customer_unique_id'].isin(recurrent_users)]
        
        interactions = df.groupby(['customer_unique_id', 'product_id']).agg({'event_weight': 'sum'}).reset_index()
        
        user_unique = interactions['customer_unique_id'].unique()
        item_unique = interactions['product_id'].unique()
        
        user_to_idx = {user: i for i, user in enumerate(user_unique)}
        idx_to_user = {i: user for i, user in enumerate(user_unique)}
        item_to_idx = {item: i for i, item in enumerate(item_unique)}
        idx_to_item = {i: item for i, item in enumerate(item_unique)}
        
        interactions['user_idx'] = interactions['customer_unique_id'].map(user_to_idx)
        interactions['item_idx'] = interactions['product_id'].map(item_to_idx)
        
        train_matrix = csr_matrix((interactions['event_weight'], (interactions['user_idx'], interactions['item_idx'])), 
                                  shape=(len(user_unique), len(item_unique)))
        
        self._save_artifacts(train_matrix, user_to_idx, idx_to_user, item_to_idx, idx_to_item)


if __name__ == "__main__":
    # Selecciona el pipeline que desees ejecutar:
    etl = UniversalETL(dataset_type='amazon')
    
    # Suponiendo que el archivo está en Dataset/Magazine_Subscriptions.json/Magazine_Subscriptions.json
    # o directamente en Dataset/Magazine_Subscriptions.json
    amazon_file = os.path.join('Magazine_Subscriptions.json', 'Magazine_Subscriptions.json')
    if not os.path.exists(os.path.join(DATA_DIR, amazon_file)):
        amazon_file = 'Magazine_Subscriptions.json' # Por si está suelto
        
    etl.run_amazon_streaming(amazon_file)
    
    # Para correr Olist, descomenta:
    # etl_olist = UniversalETL(dataset_type='olist')
    # etl_olist.run_olist_batch()
