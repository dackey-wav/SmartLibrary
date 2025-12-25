from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from . import models

def get_books(
        db: Session,
        skip: int = 0, limit: int = 100,
        sort: str | None = None, 
        genre_id: int | None = None,
        author_id: int | None = None,
        search: str | None = None
        ):
    
    query = db.query(models.Book).options(
        joinedload(models.Book.author),
        joinedload(models.Book.genre)
    )

    if genre_id is not None:
        query = query.filter(models.Book.genre_id == genre_id)

    if author_id is not None:
        query = query.filter(models.Book.author_id == author_id)
    
    if search:
        search_pattern = f"%{search}%"
        query = query.filter(
            or_(
                models.Book.title.ilike(search_pattern),
                models.Book.author.has(models.Author.name.ilike(search_pattern))
            )
        )

    if sort is not None:
        if sort == "asc":
            query = query.order_by(models.Book.title.asc())
        elif sort == "desc":
            query = query.order_by(models.Book.title.desc())   

    total_items = query.count()
    books = query.offset(skip).limit(limit).all()

    return books, total_items

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_reservations(db: Session, user_id: int, skip: int = 0, limit: int = 5):
    return db.query(models.Reservation).options(
        joinedload(models.Reservation.book).joinedload(models.Book.author),
        joinedload(models.Reservation.book).joinedload(models.Book.genre)
        ).filter(models.Reservation.user_id ==
            user_id).offset(skip).limit(limit).all()

def get_genres(db: Session):
    return db.query(models.Genre).all()

def get_authors(db: Session):
    return db.query(models.Author).all()
