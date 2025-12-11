from passlib.context import CryptContext
from app.db import SessionLocal
from app.models import Role, User

session = SessionLocal()

role_name = 'user'
role_obj = session.query(Role).filter(Role.name == role_name).first()
if not role_obj:
    role_obj = Role(name=role_name)
    session.add(role_obj)
    session.flush()

username = 'testuser'
user_obj = session.query(User).filter(User.name == username).first()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
hashed_password = pwd_context.hash("SmartLib")

if not user_obj:
    user_obj = User(
                    name=username,
                    email='test_email@smartlib.com',
                    password_hash=hashed_password,
                    role_id=role_obj.id
                        )
    session.add(user_obj)
    session.flush()

print("Test user created")
session.commit()
session.close()