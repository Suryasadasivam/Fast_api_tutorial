from typing import Optional
from fastapi import Body, FastAPI,Path,Query,HTTPException
from pydantic import BaseModel, Field
from starlette import status


app=FastAPI()

class Book:
    id:int
    title:str
    author:str
    description:str
    rating:int
    published_date:int

    def __init__(self,id, title, author, description, rating, published_date):
        self.id=id
        self.title=title
        self.author=author
        self.description=description
        self.rating=rating
        self.published_date=published_date

class BookRequest(BaseModel):
    id: Optional[int] =Field(description="Id is not needed on create", default=None)
    title:str=Field(min_length=3)
    author:str=Field(min_length=1)
    description:str=Field(min_length=1,max_length=100)
    rating:int=Field(gt=0,lt=6)
    published_date:int=Field(gt=1999,lt=2031)

    model_config={
        "json_schema_extra":{
            "example":{
                "title": "A new book",
                "author": "codingwithsurya",
                "description":"A new description of the book",
                "rating": 5,
                "published_date":2029

            }
        }

    }

BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2, 'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3, 'Master Endpoints', 'codingwithroby', 'A awesome book!', 5, 2029),
    Book(4, 'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5, 'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6, 'HP3', 'Author 3', 'Book Description', 1, 2026)
]

@app.get("/books",status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS

#Path data validation
@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_all_books(book_id:int=Path(gt=0)):
    for book in BOOKS:
        if book.id==book_id:
            return book
    raise HTTPException(status_code=404,detail="Item not found")

#query data validation
@app.get("/books/rating",status_code=status.HTTP_200_OK)
async def read_all_books_ratings(book_rating:int=Query(gt=0,lt=6)):
    book_result=[]
    for book in BOOKS:
        if book.rating==book_rating:
            book_result.append(book)
    return book_result

@app.get("/books/publish",status_code=status.HTTP_200_OK)
async def read_all_books_publish(book_rating:int=Query(gt=1999,lt=2031)):
    book_result_publish=[]
    for book in BOOKS:
        if book.rating==book_rating:
            book_result_publish.append(book)
    return book_result_publish

#Data validation 
@app.post("/create_books",status_code=status.HTTP_201_CREATED)
async def create_book(book_request:BookRequest):
    new_book=Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))

def find_book_id(book:Book):
    book.id=1 if len(BOOKS)==0 else BOOKS[-1].id+1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not found')
    
# Dhanush 
