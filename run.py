#!/usr/bin/env python3
"""
Script pour démarrer l'API de gestion de réservations de salles
"""
import uvicorn
from app.main import app

if __name__ == "__main__":
    print("🚀 Démarrage de l'API de Gestion de Réservations de Salles")
    print("📖 Documentation disponible sur : http://localhost:8000/docs")
    print("🔄 API disponible sur : http://localhost:8000")
    print("⏹️  Arrêt avec Ctrl+C")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
