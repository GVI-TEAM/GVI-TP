"""
Schémas Pydantic pour les salles - v1.1.0
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict

class SalleBase(BaseModel):
    """Schéma de base pour une salle - v1.1.0"""
    nom: str
    capacite: int
    localisation: str
    disponible: bool = True

class SalleCreate(SalleBase):
    """Schéma pour la création d'une salle."""
    pass

class SalleUpdate(BaseModel):
    """Schéma pour la mise à jour d'une salle."""
    nom: Optional[str] = None
    capacite: Optional[int] = None
    localisation: Optional[str] = None
    disponible: Optional[bool] = None

class SalleResponse(SalleBase):
    """Schéma de réponse pour une salle avec ID."""
    id: str
    
    model_config = ConfigDict(from_attributes=True)
