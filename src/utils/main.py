import os
import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import Optional, Dict

# Set up logging
logging.basicConfig(level=logging.INFO)

# Define API endpoint models
class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    username: str
    email: str

class AuthRequest(BaseModel):
    username: str
    password: str

class AuthResponse(BaseModel):
    access_token: str
    token_type: str

class Ping(BaseModel):
    message: str

# Define API routes
app = FastAPI()

@app.post("/auth/login", response_model=AuthResponse)
async def login(auth_request: AuthRequest):
    # Authenticate user
    # Replace with actual authentication logic
    username = auth_request.username
    password = auth_request.password
    if username == "admin" and password == "password":
        return {"access_token": "access_token", "token_type": "bearer"}

@app.get("/auth/ping", response_model=Ping)
async def ping():
    return {"message": "pong"}

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    # Replace with actual database query
    user = {"username": "john_doe", "email": "johndoe@example.com"}
    return user

@app.get("/items/{item_id}", response_model=User)
async def read_item(item_id: int):
    # Replace with actual database query
    item = {"username": "jane_doe", "email": "janedoe@example.com"}
    return item

@app.get("/", response_model=JSONResponse)
async def read_root():
    return {"message": "Welcome to the auth gateway!"}