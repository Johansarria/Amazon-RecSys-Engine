# Amazon RecSys Engine - Frontend 🎨

Este directorio contiene la capa de presentación visual para el motor de recomendaciones. Está construido como una aplicación **React** moderna, enfocada en la velocidad y el diseño de alta calidad.

## 🛠️ Tecnologías Utilizadas

- **Vite:** Build tool ultrarrápido para el entorno de desarrollo.
- **React (TypeScript):** Librería principal para la construcción de interfaces tipadas y modulares.
- **TailwindCSS:** Framework de utilidades CSS para un maquetado ágil.

## 🌟 Diseño e Interfaz (Design System)

La interfaz de usuario fue conceptualizada utilizando inteligencia artificial (Stitch MCP) para lograr un estilo híbrido entre **Dashboard Analítico** y **E-commerce Premium**.

- **Dark Mode Premium:** Fondo profundo (`#131314`) con acentos vibrantes en índigo y esmeralda.
- **Glassmorphism:** Tarjetas y badges con efectos de desenfoque y bordes traslúcidos (`ghost-border`).
- **Tipografías Dinámicas:** 
  - `Inter` para legibilidad técnica y datos numéricos.
  - `Newsreader` para los títulos editoriales y el logo principal.
- **Indicadores de Precisión:** Gráficos circulares SVG generados dinámicamente que visualizan el "Match Score" calculado por el backend.

## 🚀 Instalación y Ejecución Local

Para correr este frontend de manera independiente, necesitas tener **Node.js** instalado.

1. **Instalar dependencias:**
   ```bash
   npm install
   ```

2. **Levantar el servidor de desarrollo:**
   ```bash
   npm run dev
   ```

El servidor estará disponible en `http://localhost:5173/`. 

> [!IMPORTANT]
> **Requisito del Backend:**
> Para que el dashboard muestre recomendaciones reales en lugar de errores, asegúrate de tener la API de FastAPI corriendo en `http://localhost:8000`.

## 📁 Estructura del Código
- `src/App.tsx`: Layout principal, formulario de búsqueda y gestión de estados de la conexión con FastAPI.
- `src/components/MagazineCard.tsx`: Componente modular para cada revista recomendada, con animaciones hover y soporte para *fallback* de imágenes rotas.
- `src/index.css`: Inyección de directivas de TailwindCSS y variables globales del diseño.
- `tailwind.config.js`: Tokens de diseño personalizados (colores, fuentes).
