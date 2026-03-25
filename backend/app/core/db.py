from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def seed_default_user():
    from app.models.models import User
    with Session(engine) as session:
        if not session.get(User, 1):
            session.add(User(email="local@autofiller.dev"))
            session.commit()
