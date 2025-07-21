from fastapi import FastAPI
import model
from Database import engine

app=FastAPI()

model.Base.metadata.create_all(bind=engine)
