#Practicing FastAPIs

from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI() #initializing a FastAPI object

#treating it as database
book_data =  {"book_1":{"title":"Title One", "author":"Author One"},
              "book_2":{"title":"Title Two", "author":"Author Two"},
              "book_3":{"title":"Title Three", "author":"Author Three"},
              "book_4":{"title":"Title Four", "author":"Author Four"},
              "book_5":{"title":"Title Five", "author":"Author Five"}}

#This will ensure that in swagger UI, we get a drop down list
class Directions(str,Enum):
    NORTH = "North"
    SOUTH = "South"
    EAST = "East"
    WEST = "West"

@app.get("/directions/{direction_name}")
async def get_direction(direction_name: Directions):
    if direction_name == Directions.NORTH:
        return {"Direction": direction_name, "Subject":"up"}
    
    elif direction_name == Directions.SOUTH:
        return {"Direction": direction_name, "Subject":"down"}
    
    elif direction_name == Directions.EAST:
        return {"Direction": direction_name, "Subject":"right"}
    
    elif direction_name == Directions.WEST:
        return {"Direction": direction_name, "Subject":"left"}


@app.get("/") #in root url we will hit this endpoint
async def fetch_all_books():
    print(len(book_data))
    print(book_data)
    return book_data

#favorite books
@app.get("/books/mybooks")
async def fetch_favorite_book():
    return {"book_title": "my favorite book"}

#path parameters(part of the url), fetching book on id basiss
@app.get("/books/{book_id}")
async def fetch_book(book_id: int):
    return {"book_id":book_id}

@app.get("/bookname/{book_name}")
async def fetch_book_from_dictionary(book_name:str):
    return {book_name: book_data[book_name]}

#Query parameters(key:value pairs go after question mark in url)
#set the default value for the parameter in function
#optional, makes the particular parameter optional else it is mandatory
@app.get("/skipbook")
async def read_all_books_except(skip_book:Optional[str] = None):
    if skip_book:
        new_book = book_data.copy()
        del new_book[skip_book]
        return new_book
    
    return book_data


#post request method, client sends some data to store in database and server send some response.

@app.post("/createbook")
async def create_book(book_title:str, book_author:str):
    current_book_id = 0

    if len(book_data)>0:
        for book in book_data:
            x = int(book.split('_')[-1])
            if x>current_book_id:
                current_book_id = x

    book_data[f"book_{current_book_id+1}"] = {"title":book_title, "author":book_author}
    return f"Book book_{current_book_id+1} added successfully..."

#put request(updates a resource)

@app.put("/updatebook/{book_name}")
async def update_book(book_name:str,new_title:str, new_author:str):
    book_data[book_name] = {"title":new_title, "author":new_author}
    return f"Book {book_name} updated successfully..."

#delete request

@app.delete("/deletebook/{book_name}")
async def delete_book(book_name):
    del book_data[book_name]
    return f"Book {book_name} deleted successfully..."


'''
Currently we are using Path Parameters for our API calls. Create two new APIs for our current application :)

1. Create a new read book function that uses query params instead of path params.

2. Create a new delete book function that uses query params instead of path params.
'''

@app.get("/fetchbook/")
async def read_book_query_parameter(book_name: str):
    return {book_name:book_data[book_name]}

@app.delete("/deletebook/")
async def delete_book_query_parameter(book_name: str):
    del book_data[book_name]
    return f"Book {book_name} deleted successfully..."
