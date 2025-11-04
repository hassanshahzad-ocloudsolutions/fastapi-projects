#Database session + connection management

from orm import SessionLocal

#binding our sqlalchemy engine with the models, it may look lie models(python) <-> sqlalchemy engine <-> sqlite3 todo.db
   
#creating session for our databse
def get_db():
    try:
        db =  SessionLocal()
        yield db
    finally:
        db.close()
