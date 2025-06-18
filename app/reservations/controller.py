"""
Contrôleur API pour la gestion des réservations.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.reservations.schema import ReservationCreate, ReservationUpdate, ReservationResponse
from app.reservations.service import ReservationService

router = APIRouter()

@router.post("/reservations", response_model=ReservationResponse, status_code=201)
def create_reservation(
    reservation_data: ReservationCreate,
    db: Session = Depends(get_db)
):
    """Crée une nouvelle réservation."""
    # Vérifier que la salle existe
    if not ReservationService.validate_salle_exists(db, reservation_data.salle_id):
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    
    try:
        return ReservationService.create_reservation(db=db, reservation_data=reservation_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/reservations", response_model=List[ReservationResponse])
def read_reservations(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximal d'éléments à retourner"),
    db: Session = Depends(get_db)
):
    """Récupère la liste des réservations."""
    reservations = ReservationService.get_reservations(db, skip=skip, limit=limit)
    return reservations

@router.get("/reservations/{reservation_id}", response_model=ReservationResponse)
def read_reservation(reservation_id: str, db: Session = Depends(get_db)):
    """Récupère une réservation par son ID."""
    db_reservation = ReservationService.get_reservation(db, reservation_id=reservation_id)
    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Réservation non trouvée")
    return db_reservation

@router.get("/salles/{salle_id}/reservations", response_model=List[ReservationResponse])
def read_reservations_by_salle(salle_id: str, db: Session = Depends(get_db)):
    """Récupère les réservations d'une salle spécifique."""
    # Vérifier que la salle existe
    if not ReservationService.validate_salle_exists(db, salle_id):
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    
    reservations = ReservationService.get_reservations_by_salle(db, salle_id=salle_id)
    return reservations

@router.put("/reservations/{reservation_id}", response_model=ReservationResponse)
def update_reservation(
    reservation_id: str,
    reservation_data: ReservationUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour une réservation existante."""
    try:
        updated_reservation = ReservationService.update_reservation(
            db=db, 
            reservation_id=reservation_id, 
            reservation_data=reservation_data
        )
        if updated_reservation is None:
            raise HTTPException(status_code=404, detail="Réservation non trouvée")
        return updated_reservation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))