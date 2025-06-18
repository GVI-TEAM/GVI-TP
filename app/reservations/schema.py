"""
Schémas Pydantic pour les réservations.
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

class ReservationCreate(ReservationBase):
    """Schéma pour la création d'une réservation."""
    pass

class ReservationUpdate(BaseModel):
    """Schéma pour la mise à jour d'une réservation."""
    date: Optional["date"] = None
    heure: Optional["time"] = None
    utilisateur: Optional[str] = None

class ReservationResponse(ReservationBase):
    """Schéma de réponse pour une réservation avec ID."""
    id: str
    
    class Config:
        from_attributes = True