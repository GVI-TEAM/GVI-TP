"""
Services métier pour les réservations.
"""
from typing import List, Optional
from datetime import date, time
from sqlalchemy.orm import Session
from app.core.database import Salle, Reservation
from app.reservations.schema import ReservationCreate, ReservationUpdate

class ReservationService:
    """Service pour la gestion des réservations."""
    
    @staticmethod
    def get_reservation(db: Session, reservation_id: str) -> Optional[Reservation]:
        """Récupère une réservation par son ID."""
        return db.query(Reservation).filter(Reservation.id == reservation_id).first()

    @staticmethod
    def get_reservations(db: Session, skip: int = 0, limit: int = 100) -> List[Reservation]:
        """Récupère la liste des réservations."""
        return db.query(Reservation).offset(skip).limit(limit).all()

    @staticmethod
    def get_reservations_by_salle(db: Session, salle_id: str) -> List[Reservation]:
        """Récupère les réservations d'une salle spécifique."""
        return db.query(Reservation).filter(Reservation.salle_id == salle_id).all()

    @staticmethod
    def check_reservation_conflict(db: Session, salle_id: str, date_reservation: date, heure_reservation: time, exclude_id: Optional[str] = None) -> bool:
        """Vérifie s'il y a un conflit de réservation pour une salle à une date et heure données."""
        query = db.query(Reservation).filter(
            Reservation.salle_id == salle_id,
            Reservation.date == date_reservation,
            Reservation.heure == heure_reservation
        )
        
        if exclude_id:
            query = query.filter(Reservation.id != exclude_id)
        
        return query.first() is not None

    @staticmethod
    def create_reservation(db: Session, reservation_data: ReservationCreate) -> Reservation:
        """Crée une nouvelle réservation."""
        # Vérifier s'il y a un conflit
        if ReservationService.check_reservation_conflict(db, reservation_data.salle_id, reservation_data.date, reservation_data.heure):
            raise ValueError("Cette salle est déjà réservée à cette date et heure")
        
        db_reservation = Reservation(**reservation_data.model_dump())
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
        return db_reservation

    @staticmethod
    def update_reservation(db: Session, reservation_id: str, reservation_data: ReservationUpdate) -> Optional[Reservation]:
        """Met à jour une réservation existante."""
        db_reservation = ReservationService.get_reservation(db, reservation_id)
        if db_reservation:
            update_data = reservation_data.model_dump(exclude_unset=True)
            
            # Vérifier les conflits si la date, l'heure ou la salle changent
            new_salle_id = update_data.get('salle_id', db_reservation.salle_id)
            new_date = update_data.get('date', db_reservation.date)
            new_heure = update_data.get('heure', db_reservation.heure)
            
            if ReservationService.check_reservation_conflict(db, new_salle_id, new_date, new_heure, reservation_id):
                raise ValueError("Cette salle est déjà réservée à cette date et heure")
            
            for field, value in update_data.items():
                setattr(db_reservation, field, value)
            db.commit()
            db.refresh(db_reservation)
        return db_reservation

    @staticmethod
    def delete_reservation(db: Session, reservation_id: str) -> bool:
        """Supprime une réservation."""
        db_reservation = ReservationService.get_reservation(db, reservation_id)
        if db_reservation:
            db.delete(db_reservation)
            db.commit()
            return True
        return False

    @staticmethod
    def validate_salle_exists(db: Session, salle_id: str) -> bool:
        """Valide qu'une salle existe."""
        from app.salles.service import SalleService
        return SalleService.get_salle(db, salle_id) is not None
