#!/usr/bin/env python3

from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello world!"}
