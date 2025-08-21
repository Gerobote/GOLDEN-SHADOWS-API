from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRoute

from app.db import connect_to_mongo, close_mongo_connection
from app.routers.victims import router as victims_router
from app.routers.cases import router as cases_router
from app.routers.families import router as families_router
from app.routers.murder_methods import router as murder_methods_router
from app.routers.detectives import router as detectives_router
from app.routers.related_cases import router as related_cases_router
from app.routers.media_reports import router as media_reports_router  # si no tienes este archivo, comenta la línea y el include

app = FastAPI(
    title="Golden Shadows API",
    description="REST API (FastAPI + MongoDB) para Las Cariñosas.",
    version="1.1.0",
)

# Routers requeridos
app.include_router(victims_router, prefix="/victims", tags=["Victims"])
app.include_router(cases_router,   prefix="/cases",   tags=["Cases"])

# Routers adicionales de la historia
app.include_router(families_router,       prefix="/families",       tags=["Families"])
app.include_router(murder_methods_router, prefix="/murder-methods", tags=["Murder Methods"])
app.include_router(detectives_router,     prefix="/detectives",     tags=["Detectives"])
app.include_router(related_cases_router,  prefix="/related-cases",  tags=["Related Cases"])
app.include_router(media_reports_router,  prefix="/media-reports",  tags=["Media Reports"])  # comenta si no existe

# Eventos de app
@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

# Debug: listar rutas registradas
@app.get("/__routes", include_in_schema=False)
def list_routes():
    return [{"path": r.path, "methods": sorted(list(r.methods))} 
            for r in app.routes if isinstance(r, APIRoute)]

# Raíz: redirigir a Swagger
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
