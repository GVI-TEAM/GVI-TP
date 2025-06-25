import os
from sqlalchemy import create_engine, Column, String, Integer, Date, Time, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
import uuid

# Utiliser un chemin de base de données configurable
DATABASE_PATH = os.getenv("DATABASE_PATH", "./data/reservations.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Créer le répertoire data s'il n'existe pas
os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Salle(Base):
    __tablename__ = "salles"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nom = Column(String, nullable=False)
    capacite = Column(Integer, nullable=False)
    localisation = Column(String, nullable=False)
    disponible = Column(Boolean, nullable=False, default=True)

    reservations = relationship("Reservation", back_populates="salle")

class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    salle_id = Column(String, ForeignKey("salles.id"), nullable=False)
    date = Column(Date, nullable=False)
    heure = Column(Time, nullable=False)
    utilisateur = Column(String, nullable=False)
    commentaire = Column(String, nullable=True)

    salle = relationship("Salle", back_populates="reservations")

# Créer toutes les tables
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
