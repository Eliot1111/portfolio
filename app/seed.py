from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth import hash_password
from app.database import Base, engine
from app.models import Item, User


USERS = (
    ("security_user", "password123", "user"),
    ("security_admin", "admin123", "admin"),
)

ITEMS = (
    ("Demo laptop", "A laptop used in the diploma demo."),
    ("Security report", "A sample report for API testing."),
    ("Test device", "A device available for demo requests."),
)


def seed_database() -> None:
    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:
        for username, password, role in USERS:
            user = db.scalar(select(User).where(User.username == username))
            if user is None:
                db.add(
                    User(
                        username=username,
                        hashed_password=hash_password(password),
                        role=role,
                    )
                )
        db.commit()

        owner = db.scalar(select(User).where(User.username == "security_user"))
        if owner is None:
            raise RuntimeError("Seed user was not created")

        for name, description in ITEMS:
            exists = db.scalar(select(Item).where(Item.name == name))
            if exists is None:
                db.add(Item(name=name, description=description, owner_id=owner.id))
        db.commit()

    print("Database seeded successfully.")


if __name__ == "__main__":
    seed_database()
