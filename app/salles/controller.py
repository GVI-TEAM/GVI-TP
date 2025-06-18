"""
Contrôleur API pour la gestion des salles - MVP v1.0.0
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.salles.schema import SalleCreate, SalleUpdate, SalleResponse
from app.salles.service import SalleService

router = APIRouter()

@router.post("/salles", response_model=SalleResponse, status_code=201)
def create_salle(
    salle_data: SalleCreate,
    db: Session = Depends(get_db)
):
    """Crée une nouvelle salle."""
    # Vérifier l'unicité du nom
    if not SalleService.validate_salle_name_unique(db, salle_data.nom):
        raise HTTPException(status_code=400, detail="Une salle avec ce nom existe déjà")
    
    return SalleService.create_salle(db=db, salle_data=salle_data)

@router.get("/salles", response_model=List[SalleResponse])
def read_salles(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre maximal d'éléments à retourner"),
    db: Session = Depends(get_db)
):
    """Récupère la liste des salles."""
    salles = SalleService.get_salles(db, skip=skip, limit=limit)
    return salles

@router.get("/salles/{salle_id}", response_model=SalleResponse)
def read_salle(salle_id: str, db: Session = Depends(get_db)):
    """Récupère une salle par son ID."""
    db_salle = SalleService.get_salle(db, salle_id=salle_id)
    if db_salle is None:
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    return db_salle

@router.put("/salles/{salle_id}", response_model=SalleResponse)
def update_salle(
    salle_id: str,
    salle_data: SalleUpdate,
    db: Session = Depends(get_db)
):
    """Met à jour une salle existante."""
    # Vérifier si la salle existe
    db_salle = SalleService.get_salle(db, salle_id=salle_id)
    if db_salle is None:
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    
    # Vérifier l'unicité du nom si il est modifié
    if salle_data.nom and salle_data.nom != db_salle.nom:
        if not SalleService.validate_salle_name_unique(db, salle_data.nom, exclude_id=salle_id):
            raise HTTPException(status_code=400, detail="Une salle avec ce nom existe déjà")
    
    updated_salle = SalleService.update_salle(db=db, salle_id=salle_id, salle_data=salle_data)
    return updated_salle

@router.delete("/salles/{salle_id}", status_code=204)
def delete_salle(salle_id: str, db: Session = Depends(get_db)):
    """Supprime une salle."""
    success = SalleService.delete_salle(db=db, salle_id=salle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Salle non trouvée")
    return None
