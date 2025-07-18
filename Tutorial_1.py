from fastapi import FastAPI

app=FastAPI()

books=[
    {"id":"1", "title":"Book One", "author":"Author 1"},
    {"id":"2", "title":"Book Two", "author":"Author 2"},
    {"id":"3", "title":"Book Three", "author":"Author 2"},
    {"id":"4", "title":"Book Four", "author":"Author 3"},
    {"id":"5", "title":"Book Five", "author":"Author 1"}
]

@app.get("/home")
async def home_page():
    return "welcome to Fastapi tutorial"

#get method 
@app.get("/books")
async def home_page():
    return books

#dynamic path parameter
@app.get("/books/by_id/{book_id}")
async def home_page(book_id):
    for book in books:
        if book["id"]==book_id:
            return book 
    return {"error": "Book not found"}

#dynamic path parameter
@app.get("/books/by-title/{book_title}")
async def home_page(book_title):
    for book in books:
        if book["title"]==book_title:
            return book 
    return {"error": "Book not found"}





