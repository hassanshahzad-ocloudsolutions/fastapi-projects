
from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from project2.books import Book, BookNoRating
from typing import Optional
from uuid import UUID
from project2.custom_exceptions import NegativeNumberException
from starlette.responses import JSONResponse 



app = FastAPI()

books_data = [] #database

#by default keeping in 4 books data whenver get_all_books() function hits
@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request:Request, exception: NegativeNumberException):
    return JSONResponse(
        status_code= 418, 
        content={"message":"Hey, why do you want {exception.books_to_return} books"}
    )


@app.get("/")
async def get_all_books(books_to_return: Optional[int]=None):
    if len(books_data)==0:
        create_books_no_api()
    
    #if negative number of books count
    if books_to_return and books_to_return<0:
        raise NegativeNumberException(books_to_return)

    if books_to_return and len(books_data)>=books_to_return>=0:
        i = 0
        new_books = []
        while i<books_to_return:
            new_books.append(books_data[i])
            i+=1
        return new_books
    return books_data
  

'''In below function fastapi will understand that book is not a query parameter as Book class is inherited
by BaseModel, instead it will be excepting this in request body of post api as json '''
@app.post("/createbook",status_code=status.HTTP_201_CREATED)
async def create_book(book:Book):
    books_data.append(book)
    return book


@app.get("/header")
async def read_header(random_header: Optional[str] = Header(None)):
    return {"accept":random_header}


#Get book by uuid
@app.get("/getbook/{uuid}")
async def get_by_uuid(uuid: UUID):
    for book in books_data:
        if book.id == uuid:
            return book
    raise_book_not_found_exception()

@app.get("/getbook/norating/{uuid}", response_model=BookNoRating)
async def get_by_uuid_no_rating(uuid: UUID):
    for book in books_data:
        if book.id == uuid:
            return book
    raise_book_not_found_exception()

#uuid path parameter where new book data will be accepted in request body as jsons 
@app.put("/updatebook/{uuid}")
async def update_book(uuid:UUID, book_new: Book):
    for i,book in enumerate(books_data, start=0):
        if book.id == uuid:
            books_data[i] = book_new
            return book_new
    raise_book_not_found_exception()


@app.delete("/deletebook/{uuid}")
async def delete_book(uuid:UUID):
    for i,book in enumerate(books_data):
        if book.id == uuid:
            del books_data[i]
            return f"book with {uuid} id successfully deleted"
    raise_book_not_found_exception()
    
#with form fields
@app.post("/books/loginwithform")
async def book_login(user_name:str=Form(...), password:str = Form(...)):
    return {"username":user_name, "password":password}

#without form fields
@app.post("/books/loginwithoutform")
async def book_login_without(user_name:str, password:str):
    return {"username":user_name, "password":password}



#creating some sample book objects to add in the list, so we can fetch these record when get api called
def create_books_no_api():
    book1 = Book(id="ec945ff3-139c-41bc-a45d-a70975484970",
                 title="FastAPI", 
                 author="Roby", 
                 description="Learn fastapi from basics",
                 rating=100)
    
    book2 = Book(id="ec945ff3-139c-41bc-a45d-a70975484971",
                 title="Django", 
                 author="John", 
                 description="Learn django from basics",
                 rating=70)
    
    book3 = Book(id="ec945ff3-139c-41bc-a45d-a70975484972",
                 title="Assembly", 
                 author="Michael", 
                 description="Learn assembly from basics",
                 rating=60)
    
    book4 = Book(id="ec945ff3-139c-41bc-a45d-a70975484973",
                 title="Introduction to Java", 
                 author="Hennry", 
                 description="Learn java from basics",
                 rating=90)

    books_data.append(book1)
    books_data.append(book2)
    books_data.append(book3)
    books_data.append(book4)
    

def raise_book_not_found_exception():
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found", headers={"X-Header-Error":"Nothing to be seen at UUID"})


'''
We are going to create a fake authentication model for our project 2  :)



Modify our API book_login, so that it will consume an API header, that will have a username  attribute and a password attribute, and it will receive a query parameter of which book the user wants to read.

The username submitted must be called FastAPIUser and the password submitted must be test1234!

If both the username and password are valid, return the book located specified by the query parameter

If either username or password is invalid, return Invalid User

Call this new function after calling the  read_all_books just to make sure we have setup a fake inventory


'''

@app.post("/books/login/")
def login(uuid:UUID,username: Optional[str] = Header(None), password: Optional[str] = Header(None)):
    if username == "FastAPIUser" and password == "test1234!":
        for i,book in enumerate(books_data):
            return books_data[i]
    
    raise HTTPException(status_code=401, detail="User not valid")
        