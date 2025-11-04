import sys

sys.path.append("..")

from fastapi import APIRouter, Depends
from database_connection import get_db
from sqlalchemy.orm import Session
from schema import UserDetails, UserVerification
from models import User
from routers.auth import get_current_user
from custom_exceptions import get_user_exception
from passlib.context import CryptContext

router_users = APIRouter(prefix="/users", tags=["Users"], responses={404:{"description":"Not found"}})

#get all users
@router_users.get("/", response_model=list[UserDetails])
async def get_all_users(db:Session = Depends(get_db)):
    users = db.query(User).all()
    return users

#single user by path parameter
@router_users.get("/{id}", response_model=UserDetails)
async def get_all_users(id:int ,db:Session = Depends(get_db)):
    users = db.query(User).filter(User.id==id).first()
    return users

#single user by query parameter
@router_users.get("/query_parameter/", response_model=UserDetails)
async def get_all_users(id:int ,db:Session = Depends(get_db)):
    users = db.query(User).filter(User.id==id).first()
    return users


#Enhance users.py to be able to modify their current user's password, if passed by authentication


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_user_password(password, hash_password):
    return bcrypt_context.verify(password, hash_password)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_hash_password(password):
    return bcrypt_context.hash(password)


@router_users.put("/change_password/")
async def change_password(user_verification: UserVerification, user: dict = Depends(get_current_user),
                         db:Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    user_model = db.query(User).filter(User.id == user.get("id")).first()

    if user_model is not None:
        if (user_verification.username == user_model.username) and (verify_user_password(user_verification.password, user_model.hashed_password)):
            user_model.hashed_password = get_hash_password(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return "Successful"
        
        return get_user_exception()


#Enhance users.py to be able to delete their own user.

@router_users.delete("/delete/")
async def delete_user(user:dict = Depends(get_current_user), db:Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    
    user_model = db.query(User).filter(User.id == user.get("id")).first()

    if user_model:
        db.query(User).filter(User.id == user.get("id")).delete()
        db.commit()

        return "User successfully deleted"
    
    raise get_user_exception()
    

