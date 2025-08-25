from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.db.base import Base
from app.db.models import Property, Reservation
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import get_db  

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool


@pytest.fixture(scope="session")
def engine():
    eng = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        future=True,
    )
    Base.metadata.create_all(eng)
    yield eng
    Base.metadata.drop_all(eng)
    eng.dispose()

@pytest.fixture()
def db_session(engine):
    connection = engine.connect()
    trans = connection.begin()
    TestingSession = sessionmaker(bind=connection, autoflush=False, autocommit=False, future=True)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()
        trans.rollback()
        connection.close()

def _mk_property(session, **over):
    p = Property(
        title=over.get("title", "Casa Teste"),
        address_street=over.get("address_street", "Rua Alpha"),
        address_number=over.get("address_number", "123"),
        address_neighborhood=over.get("address_neighborhood", "Centro"),
        address_city=over.get("address_city", "Florianópolis"),
        address_state=over.get("address_state", "SC"),
        country=over.get("country", "Brasil"),
        rooms=over.get("rooms", 3),
        capacity=over.get("capacity", 6),
        price_per_night=over.get("price_per_night", 150),
    )
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

def _mk_reservation(session, **over):
    r = Reservation(
        property_id=over["property_id"],
        client_name=over.get("client_name", "Alice"),
        client_email=over.get("client_email", "a@example.com"),
        start_date=over.get("start_date"),
        end_date=over.get("end_date"),
        guests_quantity=over.get("guests_quantity", 2),
        is_active=over.get("is_active", True),
    )
    session.add(r)
    session.commit()
    session.refresh(r)
    return r


@pytest.fixture()
def client(db_session):
    def _get_db_override():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = _get_db_override
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

