
import sys

sys.path.append("..") # take everything from the parent directory like insted of project4.schema import CreateUser we can simply do from schema import CreateUser

from fastapi import Depends, Request, HTTPException, APIRouter
from schema import CreateUser
from models import User
from sqlalchemy.orm import Session
from database_connection import get_db
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import timedelta
from typing import Optional
from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext
from custom_exceptions import get_user_exception, token_exception

router_auth =  APIRouter(prefix ="/auth", tags=["auth"], responses={401: {"user":"Not authorized"}})

SECRETKEY =  "KlgH6AzYDeZeGwD288to79I3vTHT8wp7"
ALGORITHM = "HS256"
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/login/user")
def create_access_token(username:str, user_id:int, expire_delta:Optional[timedelta]=None):
    #payload
    encode = {"sub":username, "id":user_id}
    if expire_delta:
        expire = datetime.utcnow() + expire_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    encode.update({"exp":expire})

    return jwt.encode(encode, SECRETKEY, algorithm=ALGORITHM)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_hash_password(password):
    return bcrypt_context.hash(password)

#for authenticating the user
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def verify_user_password(password, hash_password):
    return bcrypt_context.verify(password, hash_password)

def authenticate_user(username:str, password:str, db):
    user = db.query(User).filter(User.username==username).first()
    if not user:
        return False
    if not verify_user_password(password, user.hashed_password) :
        return False
    return user 

#like signup page
@router_auth.post("/signup/user")
async def create_new_user(user:CreateUser, db:Session=Depends(get_db)):
    create_user_model = User()
    create_user_model.username = user.username #type: ignore
    create_user_model.email = user.email #type: ignore
    create_user_model.first_name = user.first_name #type: ignore
    create_user_model.last_name = user.last_name #type: ignore
    create_user_model.hashed_password = get_hash_password(user.password) #type: ignore
    create_user_model.is_active = True #type: ignore
    create_user_model.phone_number = user.phone_number

    db.add(create_user_model)
    db.commit()

    return {"Status":"Success"}

#login and generates a JWT
@router_auth.post("/login/user")
async def login_and_generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise token_exception()
    
    token_expires = timedelta(minutes=20)
    token = create_access_token(user.username, user.id, expire_delta=token_expires)
    return {"token":token}

#decoding the jwt to get id, username will be used in future for other APIs
async def get_current_user(token:str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRETKEY, algorithms=[ALGORITHM])
        username: str= payload.get("sub")
        user_id:int = payload.get("id")

        if username is None or user_id is None:
            raise get_user_exception()
        
        return {"username":username, "id":user_id}
    
    except JWTError:
        raise get_user_exception()