from datetime import date, timedelta
from random import choice, randint

from app.db import SessionLocal
from app.models import User, Book, Reservation

session = SessionLocal()

test_user = session.query(User).filter(User.name == 'testuser').first()

all_books = session.query(Book).all()
if len(all_books) < 5:
    exit()

random_books = [choice(all_books) for _ in range(5)]

if test_user and random_books:
    existing_reservations = session.query(Reservation).filter(Reservation.user_id == 
                                                              test_user.id).count()
    if existing_reservations > 0:
        print("max reservations for this user")
    else:
        for book in random_books:
            new_reservation = Reservation(
                user_id=test_user.id,
                book_id=book.id,
                reserve_date=date.today() - timedelta(days=randint(5, 20)),
                status='active'
            )
            session.add(new_reservation)

        session.commit()
        print(f"5 loans for user '{test_user.name}' created")
else:
    print("testuser or books not found")

session.close()