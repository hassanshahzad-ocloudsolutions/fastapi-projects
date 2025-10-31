#FastAPI endpoints file

from fastapi import FastAPI, Depends, HTTPException, status, Request
import models
from database_connection import get_db
from sqlalchemy.orm import Session
from custom_exceptions import NegativeNumberException
from starlette.responses import JSONResponse 
from schema import TodoAdd, TodoUpdate

app = FastAPI()

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request:Request, exception: NegativeNumberException):
    return JSONResponse(
        status_code= 400, 
        content={"message":f"{exception.todo_id} id is not allowed.."}
    )

#get all todos
@app.get("/todo")
async def get_all_todos(db: Session = Depends(get_db)):
    return db.query(models.Todo).all()

#get todo on id basis
@app.get("/todo/{todo_id}")
async def get_specific_todo(todo_id:int, db: Session = Depends(get_db)):
    if todo_id and todo_id<0:
        raise NegativeNumberException(todo_id)
    
    todo_object = db.query(models.Todo).filter(models.Todo.id== todo_id).first()
    if todo_object:
        return todo_object

    raise http_exception(todo_id)

#Get all completed or pending todos
@app.get("/todos/filter/")
async def filter_todo(filter: bool, db:Session = Depends(get_db)):
    return db.query(models.Todo).filter(models.Todo.complete==filter).all()

#creating a new todo
@app.post("/add_todo")
async def create_todo(todo: TodoAdd, db:Session=Depends(get_db)):
    todo_model = models.Todo()
    todo_model.title = todo.title #type: ignore
    todo_model.description = todo.description #type: ignore
    todo_model.priority = todo.priority #type: ignore
    todo_model.complete = todo.complete #type: ignore

    db.add(todo_model)
    db.commit()

    return {
        'status':201,
        'transaction': 'successful!'
    }

#updating existing todo
@app.put("/update_todo/{todo_id}")
async def update_todo(todo_id:int,todo:TodoUpdate, db: Session = Depends(get_db)):
    if todo_id and todo_id<0:
        raise NegativeNumberException(todo_id)
    
    todo_model = db.query(models.Todo).filter(models.Todo.id==todo_id).first()
    
    #only we can modify is the description and complete status
    if todo_model:
        todo_model.description = todo.description #type: ignore
        todo_model.complete = todo.complete #type: ignore

        db.add(todo_model)
        db.commit()

        return {
        "status":200,
        "updated_todo": {
        "id": todo_model.id,
        "title": todo_model.title,
        "description": todo_model.description,
        "priority": todo_model.priority,
        "complete": todo_model.complete
            }
        }

    raise http_exception(todo_id)


#delete a todo
@app.delete("/delete_todo{todo_id}")
async def delete_todo(todo_id:int, db:Session = Depends(get_db)):
    if todo_id and todo_id<0:
        raise NegativeNumberException(todo_id)
    
    #to check whether this record exists or not
    todo_model = db.query(models.Todo).filter(models.Todo.id == todo_id).first()

    if todo_model:
        db.query(models.Todo).filter(models.Todo.id == todo_id).delete()
        db.commit()
        return {
        'status':200,
        'transaction': 'successful!'
        }

    raise http_exception(todo_id)

      
def http_exception(todo_id):
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Todo with id {todo_id} not found...")

 

