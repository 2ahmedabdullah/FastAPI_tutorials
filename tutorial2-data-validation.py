from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()


class Class_Book:
    id: str
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


books = [
        Class_Book(1, 'CS', 'Raman VB', 'Computer Science', 5),
        Class_Book(2, 'MM', 'Chandu C', 'Maths', 3),
        Class_Book(3, 'MM', 'Shipra M', 'Maths', 2),
        Class_Book(4, 'DS', 'Pragya G', 'Data Science', 1),
        Class_Book(5, 'DS', 'Ravi B', 'Data Science', 5),
        Class_Book(6, 'DE', 'Kiran K', 'Data Engineering', 4),
        ]



# data validation here (ERROR HANDLING)
class BookRequest(BaseModel):
    id: Optional[int] = Field(title = 'id is optional')
    title: str = Field(min_length = 1)
    author: str = Field(min_length = 1)
    description: str = Field(min_length = 1, max_length = 25)
    rating: int = Field(gt = -1, lt = 6)

    #default configuration to show in SWAGGER
    class Config:
        schema_extra = {
            'example': {
                'title': 'an example title',
                'author': 'an example author',
                'description': 'an example of description',
                'rating': 5
            }
        }


def find_book_id(x: books):
    if len(books)>0:
        x.id = books[-1].id + 1
    else:
        x.id = 1
    return x


# GET REQUEST
@app.get("/books", status_code = status.HTTP_200_OK)
async def read_all_books():
    return books

# POST REQUEST
@app.post("/create-book")
async def create_book(book_request: BookRequest, status_code = status.HTTP_201_CREATED):
    new_book = Class_Book(**book_request.dict())
    # new_book = Class_Book(**book_request.model_dump()) ---- if above not working (version issues)   

    new_book_with_id = find_book_id(new_book)
    books.append(new_book_with_id)
    

# path parameter (GET REQUEST)
@app.get("/books_based_on_id/{book_id}", status_code = status.HTTP_200_OK)
async def get_book_from_id(book_id: int = Path(gt=0): # path data validation here Path(gt = 0) only applicable to path parameter
    for x in books:
        if x.id == book_id:
            return x
    # if book_id doesnot exist
    raise HTTPException(status_code = 404, detail = 'Item not Found')


# query parameter (GET REQUEST) <OPTIONAL>
@app.get("/books_based_on_rating/", status_code = status.HTTP_200_OK)
async def get_book_from_id(book_rating: int = Query(gt=0, lt=6)): # Query data validation here (applicable to query parameter)
    m = []
    for x in books:
        if x.rating >= book_rating:
            m.append(x)
    return m


# PUT REQUEST
@app.put("/update_book")
async def update_the_book(update_book: BookRequest, status_code = status.HTTP_204_NO_CONTENT):
    book_changed = False
    for i in range(len(books)):
        if books[i].id == update_book.id:
            books[i] = update_book
            book_changed = True

    # if book_id doesnot exist
    if not book_change:
        raise HTTPException(status_code = 404, detail = 'Item not Found')



# DELETE REQUEST
@app.delete("/delete_books/{book_id}", status_code = status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)): # Path validation here Path(gt = 0) only applicable to Path parameter
    book_changed = False
    for i in range(len(books)):
        print(i)
        if books[i].id == book_id:
            books.pop(i)
            book_changed = True
            break
    
    # if book_id doesnot exist
    if not book_change:
        raise HTTPException(status_code = 404, detail = 'Item not Found')
        


# uvicorn books:app --reload (web server)

