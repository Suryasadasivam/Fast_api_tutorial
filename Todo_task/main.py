from fastapi import FastAPI
import model
from Database import engine
from routers import auth,todos,admin,user


from starlette import status

app=FastAPI()

model.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(user.router)

