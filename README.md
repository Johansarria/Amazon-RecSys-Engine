# Amazon Magazine RecSys Engine 📖

Un motor de recomendaciones híbrido (Collaborative Filtering) diseñado para procesar el dataset público de "Amazon Magazine Subscriptions", con una arquitectura robusta orientada a datos y escalabilidad en memoria.

## 🎯 Arquitectura de Datos y Modelado (Data & ML)

El núcleo de este proyecto reside en su pipeline de procesamiento de datos y modelado matemático avanzado, capaz de manejar grandes volúmenes de datos superando los límites de RAM (Prevención de Out-of-Memory).

### 1. Universal ETL Pipeline (Extracción y Transformación)
- **Procesamiento de Streaming (`yield`)**: Los metadatos en formato JSON se procesan registro por registro en lugar de cargar todo el archivo en la memoria principal. Esto permite escalar el procesamiento de archivos de múltiples Gigabytes en máquinas con RAM limitada.
- **Limpieza y Filtrado (`etl_pipeline.py`)**: Extrae y vincula únicamente productos (ASINs) que poseen metadatos completos (imagen, título, categoría) junto con transacciones verificadas.
- **Sparse Matrix (CSR)**: Las interacciones usuario-ítem se comprimen en una matriz esparcida (Compressed Sparse Row). Esto reduce dramáticamente la huella en memoria, permitiendo cálculos algebraicos ultrarrápidos para la similitud del coseno y factorización.

### 2. Machine Learning Engine (Filtrado Colaborativo)
- **Modelo**: Algoritmo **ALS (Alternating Least Squares)** optimizado por la librería `implicit`.
- **Enfoque**: Filtrado Colaborativo Implícito. El sistema deduce las preferencias no solo por calificaciones explícitas, sino por las interacciones y frecuencias de lectura/suscripción.
- **Inferencia**: Vectorización pura. Al recibir un ID de usuario, se recupera en tiempo real su vector numérico desde `mapeos_ids.pkl`, se realiza la multiplicación de matrices contra los factores latentes del modelo y se devuelven los "Match Scores" de confianza.

## 💻 Stack Tecnológico
- **Data Engineering**: Python, Pandas, Scipy (Sparse Matrices), Joblib (Persistencia).
- **Machine Learning**: `implicit`, `scikit-learn`.
- **Capa de Servicio (API)**: FastAPI con CORS (Servicio escalable y tipado).
- **Capa Visual (Frontend)**: React, Vite, TailwindCSS (Design System híbrido "E-commerce & Analytics").

## 📂 Estructura del Proyecto

```text
├── api/
│   └── main.py              # Endpoints de FastAPI (Recomendaciones e Hidratación)
├── docs/                    # Documentación y Assets Visuales
│   ├── Plan de Arquitectura.pdf
│   └── dashboard_design.jpg
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes UI (MagazineCard)
│   │   └── App.tsx          # Dashboard principal de React
│   └── tailwind.config.js   # Design System (Dark Mode Premium)
├── models/
│   └── implicit_als.npz     # Pesos y factores latentes del modelo entrenado
├── processed/
│   ├── mapeos_ids.pkl       # "Piedra Rosetta" de conversión ID Amazon <-> Índice Matricial
│   ├── train_matrix.pkl     # Matriz esparcida de interacciones
│   └── asin_to_meta.pkl     # Catálogo en memoria de imágenes y metadatos
├── prototypes/              # Código heredado y experimentación temprana
│   └── streamlit_app.py     # MVP Inicial en Streamlit (Fase 4 - Inactivo)
├── scripts/
│   ├── etl_pipeline.py      # Motor Universal ETL (Manejo de Memoria / Streaming)
│   ├── train_amazon.py      # Orquestador del entrenamiento ALS
│   └── start_api.sh         # Script de despliegue local (WSL)
└── services/                
    ├── agent_service.py     # Integración (Standby) de Agente LLM Ollama
    └── firebase_service.py  # Integración (Standby) de Firestore Analytics
```

## 🚀 Uso Local

1. **Levantar el Backend (FastAPI)**
   ```bash
   cd api
   uvicorn main:app --reload
   ```
2. **Levantar el Frontend (React)**
   ```bash
   cd frontend
   npm run dev
   ```

*Nota: Asegúrese de tener el entorno virtual activo con las dependencias listadas en `requirements.txt` o `environment.yml` instaladas.*
