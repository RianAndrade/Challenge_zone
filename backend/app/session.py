from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.base import Base  # seu declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:password@db:5432/appdb"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

