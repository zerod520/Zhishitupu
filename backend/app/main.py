from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .config import ROOT, Settings
from .graph_repository import DemoGraphRepository, Neo4jGraphRepository
from .modules import knowledge_graph, data_governance, model_governance


def create_app(settings: Settings | None = None) -> FastAPI:
    settings = settings or Settings()

    @asynccontextmanager
    async def lifespan(app):
        app.state.graph = (DemoGraphRepository() if settings.graph_backend == "demo"
                           else Neo4jGraphRepository(settings))
        yield
        app.state.graph.close()

    app = FastAPI(title=settings.app_name, version="0.1.0", lifespan=lifespan)

    @app.get("/api/v1/health", tags=["系统"])
    def health():
        # Liveness only; this does not claim Neo4j is connected.
        return {"status": "ok", "version": "0.1.0", "graph_backend": settings.graph_backend,
                "database_checked": False, "prediction_integration": "not_implemented"}

    for module in (knowledge_graph, data_governance, model_governance):
        app.include_router(module.router, prefix="/api/v1")
    # Mount last, so API and OpenAPI routes take priority.
    app.mount("/", StaticFiles(directory=ROOT / "frontend", html=True), name="frontend")
    return app

app = create_app()
