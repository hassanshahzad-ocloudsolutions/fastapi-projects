#FastAPI endpoints file
#Only todos table is being used here
import sys
sys.path.append("..")

from fastapi import FastAPI, Depends
from routers import auth, todo, users
import models
from orm import engine
from company import companyapis, dependencies


app = FastAPI()

models.Base.metadata.create_all(bind=engine) 

app.include_router(auth.router_auth)
app.include_router(todo.router_todo)
app.include_router(companyapis.router_company,
                    prefix="/companyapis",
                    tags=["External APIs Example"],
                    dependencies= [Depends(dependencies.get_token_header)],
                    responses= {418:{"description":"Internal use only"}})

app.include_router(users.router_users)





 

