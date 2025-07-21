from fastapi import Body, FastAPI

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

#dynamic query parameter
@app.get("/books/by-author")
async def home_page(book_author):
    for book in books:
        if book["author"]==book_author:
            return book 
    return {"error": "Book not found"}


# post request 

@app.post("/books/addbooks")
async def home_page(new_book=Body()):
    books.append(new_book)
    return {"message": "Book has been successfully updated"}

#put method
@app.put("/books/update")
async def home_page(update_book=Body()):
    for index, book in enumerate(books):
        if book["id"] == update_book["id"]:
            books[index] = update_book  # ✅ Update the list element directly
            return {"message": "Book updated successfully"}
    return {"error": "Book not found"}

#delete method 
@app.delete("/books/delete/{book_id}")
async def delete_book(book_id: str):
    for index, book in enumerate(books):
        if book["id"] == book_id:
            books.pop(index)  # ✅ Removes the book from the list
            return {"message": "Book deleted successfully"}
    return {"error": "Book not found"}







