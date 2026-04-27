import json
import os
import joblib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, 'Dataset')
OUTPUT_DIR = os.path.join(BASE_DIR, 'processed')

def extract_metadata():
    print("Extrayendo metadatos de Amazon...")
    meta_path = os.path.join(DATA_DIR, 'meta_Magazine_Subscriptions.json', 'meta_Magazine_Subscriptions.json')
    
    asin_to_meta = {}
    
    with open(meta_path, 'r', encoding='utf-8') as f:
        for line in f:
            data = json.loads(line)
            asin = data.get('asin')
            if asin:
                title = data.get('title', 'Sin título')
                images = data.get('imageURLHighRes', [])
                img_url = images[0] if images else "https://via.placeholder.com/150"
                category = data.get('category', [])
                cat_str = category[0] if category else "General"
                
                asin_to_meta[asin] = {
                    'title': title,
                    'image': img_url,
                    'category': cat_str
                }
    
    joblib.dump(asin_to_meta, os.path.join(OUTPUT_DIR, 'asin_to_meta.pkl'))
    print(f"Metadatos extraídos para {len(asin_to_meta)} productos.")

if __name__ == '__main__':
    extract_metadata()
