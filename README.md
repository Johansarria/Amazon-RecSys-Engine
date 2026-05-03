# Universal RecSys Engine 📖

Un motor de recomendaciones híbrido (Collaborative Filtering) agnóstico de dominio, diseñado para procesar grandes volúmenes de datos mediante una arquitectura robusta orientada a escalabilidad en memoria y **Código Limpio (Clean Architecture)**.

## 🎯 Arquitectura de Datos y Modelado (Data & ML)

El núcleo de este proyecto reside en su pipeline de procesamiento de datos y modelado matemático avanzado, ahora organizado bajo principios **SOLID** para garantizar mantenibilidad.

### 1. Universal ETL Pipeline (Extracción y Transformación)
- **Procesamiento de Streaming (`yield`)**: Los metadatos se procesan registro por registro para evitar Out-of-Memory.
- **Sparse Matrix (CSR)**: Las interacciones usuario-ítem se comprimen en una matriz esparcida para cálculos algebraicos ultrarrápidos.

### 2. Machine Learning Engine (Filtrado Colaborativo)
- **Modelo**: Algoritmo **ALS (Alternating Least Squares)** optimizado por la librería `implicit`.
- **Inferencia**: Vectorización pura con recuperación en tiempo real de vectores numéricos.

## 💻 Stack Tecnológico
- **Backend**: Python 3.11, FastAPI (Tipado fuerte y validación con Pydantic).
- **Machine Learning**: `implicit`, `scikit-learn`, `scipy`, `pandas`.
- **Frontend**: React, Vite, TailwindCSS (Design System Premium).
- **Pruebas**: Pytest (Unitarias, Integración y Mocking).

## 📂 Estructura del Proyecto (Clean Architecture)

```text
├── analytics/               # Módulos de análisis avanzado (Detección de anomalías)
├── api/                     # Capa de Presentación (Web)
│   ├── routes/              # Endpoints modularizados por dominio
│   └── main.py              # Punto de entrada de la API
├── core/                    # Configuración global y utilidades transversales
├── domain/                  # Entidades y Schemas (DTOs) para tipado fuerte
├── infrastructure/          # Adaptadores y cargadores de recursos (Models, DB)
├── services/                # Lógica de Negocio (Recommendation Engines)
├── models/                  # Binarios de modelos entrenados (.pkl, .npz)
├── processed/               # Datasets procesados y mapeos de índices
├── scripts/                 # Pipelines de ETL y entrenamiento
└── tests/                   # Suite de pruebas automatizadas
```

## 🚀 Uso Local

1. **Levantar el Backend (FastAPI)**
   ```bash
   # Desde la raíz del proyecto
   python api/main.py
   ```
2. **Levantar el Frontend (React)**
   ```bash
   cd frontend
   npm run dev
   ```

## 🧪 Pruebas
El proyecto cuenta con una suite de pruebas automatizadas. Para ejecutarlas:
```bash
$env:PYTHONPATH = "."; pytest tests/
```

---
Desarrollado por **Johan Sarria** siguiendo la [Guía Maestra de Agentes IA](AGENTES.md).