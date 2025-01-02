from fastapi import FastAPI
from database import engine
import models
from routes import router
from sqlmodel import SQLModel, create_engine

# Create the database tables
SQLModel.metadata.create_all(bind=engine)

app = FastAPI()

# Include the routes
app.include_router(router)

# To run the application, use: uvicorn main:app --reload