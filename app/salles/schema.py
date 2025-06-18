"""
Schémas Pydantic pour les salles - MVP v1.0.0
"""
from typing import Optional
from pydantic import BaseModel

class SalleBase(BaseModel):
    """Schéma de base pour une salle - MVP v1.0.0"""
    nom: str
    capacite: int
    localisation: str

class SalleCreate(SalleBase):
    """Schéma pour la création d'une salle."""
    pass

class SalleUpdate(BaseModel):
    """Schéma pour la mise à jour d'une salle."""
    nom: Optional[str] = None
    capacite: Optional[int] = None
    localisation: Optional[str] = None

class SalleResponse(SalleBase):
    """Schéma de réponse pour une salle avec ID."""
    id: str
    
    class Config:
        from_attributes = True
