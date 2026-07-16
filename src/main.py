from .database import engine, Base, get_db
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy.orm import Session
import logging
from src import models
from fastapi import FastAPI, Depends, HTTPException
from typing import Annotated

Base.metadata.create_all(bind=engine)


ALLOWED_SECTORS = [
    "IT",
    "Banking",
    "Healthcare",
    "Manufacturing",
    "Retail"
]


class Customer_Base(BaseModel):

    name: Annotated[
        str,
        Field(
            min_length=3,
            max_length=100
        )
    ]

    email: EmailStr
    company: Annotated[str,Field(min_length=2, max_length=100)]

    phone: Annotated[
        str,
        Field(
            pattern=r"^[6-9]\d{9}$"
        )
    ]

    yearly_sale: Annotated[
        float,
        Field(
            gt=0,
            le=1000000000
        )
    ]

    sector: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value):

        value = value.strip()

        if not value:
            raise ValueError(
                "Name cannot be empty"
            )

        if not value.replace(" ", "").isalpha():
            raise ValueError(
                "Name must contain only alphabets"
            )

        return value


def assign_grade_category(yearly_sale: float):

    if yearly_sale >= 100000000:
        return "A+", "Platinum"

    elif yearly_sale >= 50000000:
        return "A", "Gold"

    elif yearly_sale >= 10000000:
        return "B", "Silver"

    else:
        return "C", "Bronze"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/customer.log"),
        logging.StreamHandler()
    ],
    force=True
)

logger = logging.getLogger(__name__)

app = FastAPI()



@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/customer")
def home(c: Customer_Base, db: Session = Depends(get_db)):

    existing_customer = db.query(models.CUSTOMERS).filter(
        models.CUSTOMERS.email == c.email
    ).first()

    if existing_customer:
        logger.error(f"Email already exists: {c.email}")
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    if c.sector not in ALLOWED_SECTORS:
        logger.error(f"Invalid sector received: {c.sector}")
        raise HTTPException(
            status_code=400,
            detail=f"Sector must be one of {ALLOWED_SECTORS}"
        )

    grade, category = assign_grade_category(c.yearly_sale)

    try:

        new = models.CUSTOMERS(
            name=c.name,
            company=c.company,
            email=c.email,
            phone=c.phone,
            yearly_sale=c.yearly_sale,
            sector=c.sector,
            grade=grade,
            category=category
        )

        db.add(new)
        db.commit()
        db.refresh(new)

        logger.info(f"Customer created id={new.id}")

        return new

    except Exception as e:
        db.rollback()
        logger.exception(f"Database Error: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal Server Error"
        )


@app.get("/customer2")
def home2(db: Session = Depends(get_db)):
    customers = db.query(models.CUSTOMERS).all()
    logger.info("Fetched all customers")
    return customers


@app.get("/customer2/{id}")
def home5(id: int,db: Session = Depends(get_db)):

    customer = db.query(models.CUSTOMERS).filter(
        models.CUSTOMERS.id == id
    ).first()

    if customer is None:
        logger.error(f"Customer id={id} not found")
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    logger.info(f"Customer id={id} fetched")

    return customer


@app.put("/customer3/{id}")
def home3(id: int,db: Session = Depends(get_db)):

    customer = db.query(models.CUSTOMERS).filter(
        models.CUSTOMERS.id == id
    ).first()

    if customer is None:
        logger.error(f"Customer ID={id} not found")
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    if c.sector not in ALLOWED_SECTORS:
        logger.error(f"Invalid sector received: {c.sector}")
        raise HTTPException(
            status_code=400,
            detail=f"Sector must be one of {ALLOWED_SECTORS}"
        )

    grade, category = assign_grade_category(c.yearly_sale)

    customer.name = c.name
    customer.company = c.company
    customer.email = c.email
    customer.phone = c.phone
    customer.yearly_sale = c.yearly_sale
    customer.sector = c.sector
    customer.grade = grade
    customer.category = category

    db.commit()
    db.refresh(customer)

    logger.info(f"Updated customer ID={id}")

    return {
        "message": "Customer updated successfully",
        "customer": customer
    }


@app.delete("/customer4/{id}")
def home4(id: int,db: Session = Depends(get_db)):

    customer = db.query(models.CUSTOMERS).filter(
        models.CUSTOMERS.id == id
    ).first()

    if customer is None:
        logger.error(f"Customer ID={id} not found")
        raise HTTPException(
            status_code=404,
            detail="Customer not found"
        )

    db.delete(customer)
    db.commit()

    logger.info(f"Deleted customer ID={id}")

    return {
        "message": "Customer deleted successfully"
    }


@app.get("/customers/category/{category}")
def get_customers_by_category(
    category: str,
    db: Session = Depends(get_db)
):

    customers = db.query(models.CUSTOMERS).filter(
        models.CUSTOMERS.category.ilike(category)
    ).all()

    if not customers:
        logger.error(f"No customers found for category {category}")
        raise HTTPException(
            status_code=404,
            detail="No customers found"
        )

    logger.info(f"Fetched customers for category {category}")

    return customers