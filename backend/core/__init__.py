from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.endpoints.graph import router as graph_router
from core.endpoints.simulation import router as simulation_router
from core.endpoints.report import router as report_router
from core.endpoints.ws import router as ws_router

def create_app() -> FastAPI:
    app = FastAPI(title="Swarm-Sim Engine MVP")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(graph_router, prefix="/api/graph")
    app.include_router(simulation_router, prefix="/api/simulation")
    app.include_router(report_router, prefix="/api/report")
    app.include_router(ws_router, prefix="/api/ws/simulation")

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
