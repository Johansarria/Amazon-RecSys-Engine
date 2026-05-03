from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import recommendations
from core.config import settings

def get_application() -> FastAPI:
    _app = FastAPI(title=settings.PROJECT_NAME)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    _app.include_router(recommendations.router, prefix=settings.API_V1_STR, tags=["recommendations"])
    # Fallback legacy support for root-level routes if needed, 
    # but strictly we should use the versioned API.
    _app.include_router(recommendations.router, tags=["recommendations"])

    @_app.get("/")
    def read_root():
        return {
            "status": "online", 
            "message": "Amazon Recommendation System API",
            "version": "1.0.0"
        }

    return _app

app = get_application()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
