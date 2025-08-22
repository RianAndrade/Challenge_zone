from sqlalchemy import String, Integer, Float, Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.base import Base


class Property(Base):
    __tablename__ = "properties"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    address_street: Mapped[str] = mapped_column(String(255), nullable=False)
    address_number: Mapped[str] = mapped_column(String(50), nullable=False)
    address_neighborhood: Mapped[str] = mapped_column(String(100), nullable=False)
    address_city: Mapped[str] = mapped_column(String(100), nullable=False)
    address_state: Mapped[str] = mapped_column(String(50), nullable=False)
    country: Mapped[str] = mapped_column(String(50), nullable=False)

    rooms: Mapped[int] = mapped_column(Integer, nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    price_per_night: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)

    reservations: Mapped[list["Reservation"]] = relationship(
    back_populates="property",
    cascade="all, delete-orphan",
    )


class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    #property_id: Mapped[int] = mapped_column( ForeignKey(properties.id, ), nullable=False)
    client_name: Mapped[str] = mapped_column(String(255), nullable=False)
    client_email: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    guests_quantity: Mapped[int] = mapped_column(Integer, nullable=False)

    property: Mapped["Property"] = relationship(back_populates="reservations")


'''
    verificar depois, esta dando algum erro semantico

    __table_args__ = (
        CheckConstraint("guests_quantity >= 0", name="ck_users"),
        CheckConstraint("start_date <= end_date", name="ck_users_date_range"),
    )

'''
