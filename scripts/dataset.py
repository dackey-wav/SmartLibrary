import kagglehub
import pandas as pd
from app.db import SessionLocal, engine
from app.models import Book, Author, Genre
import random

path = kagglehub.dataset_download("lukaanicin/book-covers-dataset")
print("Path to dataset files:", path)

df = pd.read_csv('data\main_dataset.csv')
session = SessionLocal()

processed_isbn = set()

for idx, row in df.iterrows():
    try:
        if idx % 100 == 0:
            print(f'{idx} of {len(df)} records processed. Book: {row['name']}')

        isbn = str(row['isbn'])
        if isbn in processed_isbn:
            continue
        processed_isbn.add(isbn)

        if row['author'] is not None:     
            author_name = str(row['author'])
        else:
            author_name = 'Not specified'
        
        author_obj = session.query(Author).filter(Author.name == author_name).first()
        if not author_obj:
            author_obj = Author(name=author_name)
            session.add(author_obj)
            session.flush()

        genre_name = str(row['category'])
        genre_obj = session.query(Genre).filter(Genre.name == genre_name).first()
        if not genre_obj:
            genre_obj = Genre(name=genre_name)
            session.add(genre_obj)
            session.flush()

        session.add(Book(
            title=row['name'],
            isbn=isbn,
            author_id=author_obj.id,
            genre_id=genre_obj.id,
            count=random.randint(1, 10),
            cover_path=row['img_paths']
            ))
    except Exception as e:
        print(f"Ошибка при обработке строки {idx} (ISBN: {row['isbn']}): {e}")
        session.rollback()
    

session.commit()
session.close()