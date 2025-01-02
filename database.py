from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.declarative import declarative_base

# # Database setup
# DATABASE_URL = "mysql+mysqlconnector://root:LMNopq%40123@localhost/mydatabase"  # Update with your credentials
# engine = create_engine(DATABASE_URL)
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # Dependency to get the database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()




# Database setup
DATABASE_URL = "mysql+mysqlconnector://root:LMNopq%40123@localhost/mydatabase"  # Update with your credentials
engine = create_engine(DATABASE_URL)

# Dependency to get the database session
def get_db():
    with Session(engine) as session:
        yield session

