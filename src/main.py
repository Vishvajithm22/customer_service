from .database import engine,Base,get_db
from pydantic import BaseModel
from sqlalchemy.orm import Session
import logging
from src import models
from fastapi import FastAPI,Depends,HTTPException

Base.metadata.create_all(bind=engine)

class Customer_Base(BaseModel):
    email:str
    phone:str
    name:str

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/customer.log"),
        logging.StreamHandler()
    ],
    force=True
)
logger = logging.getLogger(__name__)
app=FastAPI()
@app.post("/customer")
def home(c:Customer_Base,db:Session=Depends(get_db)):
    existing_customer=db.query(models.CUSTOMERS).filter(models.CUSTOMERS.email==c.email).first()
    if existing_customer:
        logger.error(f"Email already exits:{c.email}")
        raise HTTPException(status_code=400,detail="Email already exits")
    try:
        new=models.CUSTOMERS(**c.model_dump())
        db.add(new)
        db.commit()
        db.refresh(new)
        logger.info(f"Customer created id={new.id}")
        return new
    except Exception as e:
        logger.exception(f"Database Error: {e}")
        raise HTTPException(status_code=500,detail="Internal Server Error")

@app.get("/customer2")
def home2(db:Session=Depends(get_db)):
    new=db.query(models.CUSTOMERS).all()
    logger.info(f"feteched all")
    return new

@app.get("/customer2/{id}")
def home5(id:int,db:Session=Depends(get_db)):
    new=db.query(models.CUSTOMERS).filter(models.CUSTOMERS.id==id).first()
    if new is None:
        logger.error(f"customer id={id} not found")
        raise HTTPException(status_code=404,detail="Customer not found")
    logger.info(f"customer id={id} feteched")
    return new
@app.put("/customer3/{id}")
def home3(id:int,c:Customer_Base,db:Session=Depends(get_db)):
    new=db.query(models.CUSTOMERS).filter(models.CUSTOMERS.id==id)
    cus=new.first()
    if cus is None:
        logger.error(f"Customer ID={id} not found")
        raise HTTPException(status_code=404,detail="Customer not found")
    new.update(c.model_dump())
    db.commit()
    logger.info(f"Updated customer ID={id}")
    return {"message":"Customer updated successfully"}
@app.delete("/customer4/{id}")
def home4(id:int,db:Session=Depends(get_db)):

    new= db.query(models.CUSTOMERS).filter(models.CUSTOMERS.id == id).first()

    if new is None:
        logger.error(f"Customer ID={id} not found")
        raise HTTPException(status_code=404,detail="Customer not found")
    db.delete(new)
    db.commit()
    logger.info(f"Deleted customer ID={id}")
    return {"message":"Customer deleted successfully"}