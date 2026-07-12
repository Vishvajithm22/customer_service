from .database import Base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy import func
from enum import Enum as PyEnum
from sqlalchemy import Enum


class CUSTOMERS(Base):
    __tablename__ = "customers"

    id = Column(Integer, autoincrement=True, primary_key=True)

    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    company = Column(String, nullable=False)
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

class UserRole(PyEnum):
    ADMIN = "ADMIN"
    MANAGER = "MANAGER"
    USER = "USER"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    hashed_password = Column(String, nullable=False)

    role = Column(
        Enum(UserRole),
        default=UserRole.USER,
        nullable=False
    )