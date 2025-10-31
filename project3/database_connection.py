#Database session + connection management

from orm import engine, SessionLocal
import models

#binding our sqlalchemy engine with the models, it may look lie models(python) <-> sqlalchemy engine <-> sqlite3 todo.db
def connection():
    models.Base.metadata.create_all(bind=engine) #automatically Create SQL commands run to create all tables defined in models.py

#creating session for our databse
def get_db():
    try:
        db =  SessionLocal()
        yield db
    finally:
        db.close()

connection()