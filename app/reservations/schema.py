"""
Schémas Pydantic pour les réservations - v1.1.0
"""
from typing import Optional
from datetime import date, time
from pydantic import BaseModel

class ReservationBase(BaseModel):
    """Schéma de base pour une réservation."""
    salle_id: str
    date: date
    heure: time
    utilisateur: str
    commentaire: Optional[str] = None

class ReservationCreate(ReservationBase):
    """Schéma pour la création d'une réservation."""
    pass

class ReservationUpdate(BaseModel):
    """Schéma pour la mise à jour d'une réservation."""
    date: Optional["date"] = None
    heure: Optional["time"] = None
    utilisateur: Optional[str] = None
    commentaire: Optional[str] = None

class ReservationResponse(ReservationBase):
    """Schéma de réponse pour une réservation avec ID."""
    id: str
    
    class Config:
        from_attributes = True