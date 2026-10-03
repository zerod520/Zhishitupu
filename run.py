import uvicorn
from backend.app.config import Settings

if __name__ == "__main__":
    settings = Settings()
    uvicorn.run("backend.app.main:app", host=settings.host, port=settings.port, reload=settings.reload)
