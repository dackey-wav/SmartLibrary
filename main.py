from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app import crud, models, schemas
from app.db import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/dataset", StaticFiles(directory=r"data\dataset"), name="dataset")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/api/books/", response_model=schemas.BookPage)
def read_books(
    skip: int = 0,
    limit: int = 8,
    db: Session = Depends(get_db), 
    genre_id: int | None = None,
    author_id: int | None = None,
    search: str | None = None,
    sort: str | None = None
    ):

    books, total_items = crud.get_books(
        db, skip=skip, limit=limit, genre_id=genre_id,
        author_id=author_id, search=search, sort=sort)

    return {"items": books, "total_items": total_items, "skip": skip, "limit": limit}


@app.get("/api/users/{user_id}/reservations/", response_model=list[schemas.Reservation])
def read_user_reservations(user_id: int, db: Session = Depends(get_db)):
    reservations = crud.get_user_reservations(db, user_id=user_id)
    return reservations


@app.get("/api/genres/", response_model=list[schemas.Genre])
def read_genres(db: Session = Depends(get_db)):
    genres = crud.get_genres(db)
    return genres


@app.get("/api/authors/", response_model=list[schemas.Author])
def read_authors(db: Session = Depends(get_db)):
    authors = crud.get_authors(db)
    return authors