"""
Services métier pour les salles - MVP v1.0.0
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.core.database import Salle
from app.salles.schema import SalleCreate, SalleUpdate

class SalleService:
    """Service pour la gestion des salles - MVP v1.0.0"""
    
    @staticmethod
    def get_salle(db: Session, salle_id: str) -> Optional[Salle]:
        """Récupère une salle par son ID."""
        return db.query(Salle).filter(Salle.id == salle_id).first()

    @staticmethod
    def get_salles(db: Session, skip: int = 0, limit: int = 100, disponible: Optional[bool] = None) -> List[Salle]:
        """Récupère la liste des salles avec filtrage optionnel par disponibilité."""
        query = db.query(Salle)
        if disponible is not None:
            query = query.filter(Salle.disponible == disponible)
        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_salle_by_nom(db: Session, nom: str) -> Optional[Salle]:
        """Récupère une salle par son nom."""
        return db.query(Salle).filter(Salle.nom == nom).first()

    @staticmethod
    def create_salle(db: Session, salle_data: SalleCreate) -> Salle:
        """Crée une nouvelle salle."""
        db_salle = Salle(**salle_data.model_dump())
        db.add(db_salle)
        db.commit()
        db.refresh(db_salle)
        return db_salle

    @staticmethod
    def update_salle(db: Session, salle_id: str, salle_data: SalleUpdate) -> Optional[Salle]:
        """Met à jour une salle existante."""
        db_salle = SalleService.get_salle(db, salle_id)
        if db_salle:
            update_data = salle_data.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_salle, field, value)
            db.commit()
            db.refresh(db_salle)
        return db_salle

    @staticmethod
    def delete_salle(db: Session, salle_id: str) -> bool:
        """Supprime une salle."""
        db_salle = SalleService.get_salle(db, salle_id)
        if db_salle:
            db.delete(db_salle)
            db.commit()
            return True
        return False
    
    @staticmethod
    def validate_salle_name_unique(db: Session, nom: str, exclude_id: Optional[str] = None) -> bool:
        """Valide que le nom de la salle est unique."""
        query = db.query(Salle).filter(Salle.nom == nom)
        if exclude_id:
            query = query.filter(Salle.id != exclude_id)
        return query.first() is None
