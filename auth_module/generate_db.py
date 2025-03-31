import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from auth_module.auth_models import Base, UserDB
from auth_module.user_store import hash_password

# Database path inside auth_module
DB_PATH = os.path.join(os.path.dirname(__file__), "eddie_users.db")
DATABASE_URL = f"sqlite:///{DB_PATH}"

def get_db_session():
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    return sessionmaker(bind=engine)()

def create_database():
    if os.path.exists(DB_PATH):
        print("[!] Database already exists at:", DB_PATH)
        return
    print("[+] Creating database and tables...")
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    print("[+] Done. Database created at:", DB_PATH)

def seed_users():
    db = get_db_session()
    if not db.query(UserDB).filter(UserDB.username == "alice").first():
        alice = UserDB(username="alice", hashed_password=hash_password("password123"), role="admin")
        bob = UserDB(username="bob", hashed_password=hash_password("password456"), role="user")
        db.add_all([alice, bob])
        db.commit()
        print("[+] Seeded users: alice (admin), bob (user)")
    else:
        print("[!] Default users already exist. Skipping seeding.")

def add_user_prompt():
    db = get_db_session()

    print("\n[+] Add a new user")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    confirm = input("Confirm password: ").strip()
    role = input("Role (user/admin): ").strip().lower()

    if password != confirm:
        print("[!] Passwords do not match.")
        return

    if role not in ["user", "admin"]:
        print("[!] Role must be 'user' or 'admin'.")
        return

    if db.query(UserDB).filter(UserDB.username == username).first():
        print(f"[!] User '{username}' already exists.")
        return

    hashed = hash_password(password)
    user = UserDB(username=username, hashed_password=hashed, role=role)
    db.add(user)
    db.commit()
    print(f"[+] User '{username}' added with role '{role}'.")

def remove_user_prompt():
    db = get_db_session()
    username = input("Username to remove: ").strip()
    user = db.query(UserDB).filter(UserDB.username == username).first()

    if not user:
        print(f"[!] User '{username}' does not exist.")
        return

    db.delete(user)
    db.commit()
    print(f"[+] User '{username}' has been removed.")

def main_menu():
    while True:
        print("\n=== Eddie User DB Tool ===")
        print("1. Create database")
        print("2. Seed default users (alice, bob)")
        print("3. Add a new user")
        print("4. Remove a user")
        print("5. Exit")
        choice = input("Select an option: ").strip()

        if choice == "1":
            create_database()
        elif choice == "2":
            seed_users()
        elif choice == "3":
            add_user_prompt()
        elif choice == "4":
            remove_user_prompt()
        elif choice == "5":
            print("Bye!")
            break
        else:
            print("[!] Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
