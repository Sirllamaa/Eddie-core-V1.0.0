import bcrypt
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from auth_module.auth_models import UserDB, User, Base
from typing import Optional

DATABASE_URL = "sqlite:///./auth_module/eddie_users.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine)

# Create DB + users table
Base.metadata.create_all(bind=engine)

def get_db_session():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    return sessionmaker(bind=engine)()

# ----- Password Hashing -----
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode("utf-8"), hashed_password.encode("utf-8"))

# ----- DB Logic -----
def get_user(username: str):
    db: Session = SessionLocal()
    user = db.query(UserDB).filter(UserDB.username == username).first()
    db.close()
    return user

def authenticate_user(username: str, password: str) -> Optional[User]:
    print(f"Authenticating user: {username}")  # Debugging line
    print(f"Password: {password}")  # Debugging line
    db = SessionLocal()
    user = db.query(UserDB).filter(UserDB.username == username).first()
    db.close()

    if not user or not verify_password(password, user.hashed_password):
        return None
    return User(username=user.username, role=user.role)


# ----- Seeding sample users -----
# def seed_users():
#     db = SessionLocal()
#     if not get_user("alice"):
#         user1 = UserDB(username="alice", hashed_password=hash_password("password123"), role="admin")
#         user2 = UserDB(username="bob", hashed_password=hash_password("password456"), role="user")
#         db.add_all([user1, user2])
#         db.commit()
#         print("[+] Seeded default users.")

