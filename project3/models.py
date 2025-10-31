#ORM table definitions (Data layer)

from orm import Base
from sqlalchemy import Boolean, Column, Integer, String
 
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False) 


