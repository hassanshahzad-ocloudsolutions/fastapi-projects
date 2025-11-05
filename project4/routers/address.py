import sys
sys.path.append("...")

from fastapi import Depends, APIRouter
from typing import Optional
import models
from sqlalchemy.orm import Session
from .auth import get_current_user
from custom_exceptions import get_user_exception
from database_connection import get_db
from schema import AddressAdd
from models import Address, User


router_address = APIRouter(prefix="/address", tags = ["Address"], responses={404:{"details":"Not found"}})

@router_address.post("/")
async def create_address(address:AddressAdd, 
                         user: dict = Depends(get_current_user),
                         db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception
    
    address_model = Address()
    address_model.address1 = address.address1
    address_model.address2 = address.address2
    address_model.city = address.city
    address_model.state = address.state
    address_model.country = address.country
    address_model.postal_code = address.postal_code
    address_model.apt_num = address.apt_num

    db.add(address_model)
    db.flush() # stagged not yet committed, id is associated with the address_model

    #adding this address id as foreign key inside users table addres_id field who logged in

    user_model = db.query(User).filter(User.id==user.get("id")).first()
    user_model.address_id = address_model.id

    db.add(user_model)
    db.commit()

    return {"Details":"Success"}

