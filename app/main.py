"""
Application principale FastAPI pour la gestion des réservations de salles.
"""
from fastapi import FastAPI
from app.salles.controller import router as salles_router
from app.reservations.controller import router as reservations_router

app = FastAPI(
    title="API Gestion Réservations de Salles",
    description="API REST pour gérer les réservations de salles dans un établissement",
    version="1.0.0"
)

# Inclusion des routes
app.include_router(salles_router, prefix="/api/v1", tags=["salles"])
app.include_router(reservations_router, prefix="/api/v1", tags=["reservations"])

@app.get("/")
async def root():
    """Point d'entrée de l'API"""
    return {
        "message": "API Gestion Réservations de Salles",
        "version": "1.0.0",
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Point de contrôle de santé de l'API"""
    return {"status": "healthy"}
