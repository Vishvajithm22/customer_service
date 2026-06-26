from .database import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import func


class CUSTOMERS(Base):
    __tablename__ = "customers"

    id = Column(Integer, autoincrement=True, primary_key=True)

    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=False)

    yearly_sale = Column(Float, nullable=False)
    sector = Column(String, nullable=False)
    grade = Column(String, nullable=False)
    category = Column(String, nullable=False)

    created_at = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now()
    )