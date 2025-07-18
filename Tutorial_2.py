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
    return Books

#Path validation
@app.get("/books/{book_id}",status_code=status.HTTP_200_OK)
async def read_all_books(book_id:int=Path(gt=0)):
    for book in BOOKS:
        if book.id==book_id:
            return book
    raise HTTPException(status_code=404,detail="Item not found")


