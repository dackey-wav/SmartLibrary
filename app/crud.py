from sqlalchemy.orm import Session
from . import models

def get_books(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Book).offset(skip).limit(limit).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_reservations(db: Session, user_id: int, skip: int = 0, limit: int = 5):
    return db.query(models.Reservation).filter(models.Reservation.user_id ==
            user_id).offset(skip).limit(limit).all()