#Engine setup (DB connection details)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

'''creating sqlalchmey engine, that will help us in establishing connection between database and fastapi application.
SQLAlchemy is ORM(Object Relational Mapper)'''

engine = create_engine(SQLALCHEMY_DATABASE_URL, 
                       connect_args={"check_same_thread":False})

#database session
#sessionmaker is a class factory whereas SessionLocal is class not object here, we will create its objects later 
SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)


Base = declarative_base() #ensures that any class inheriting Base, is a table.