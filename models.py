from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from database import engine

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

Base = declarative_base()

# # User model
# class User(Base):
#     __tablename__ = "rusers"

#     id = Column(Integer, primary_key=True, index=True)
#     username = Column(String(255), unique=True, index=True)
#     hashed_password = Column(String(255))
#     role_id = Column(Integer, ForeignKey('roles.id'))

#     role = relationship("Role")

# # Role model
# class Role(Base):
#     __tablename__ = "roles"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), unique=True, index=True)



# Role model
class Role(SQLModel, table=True):
    __tablename__ = "roles"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, unique=True, index=True)

    users: List["User"] = Relationship(back_populates="role")
    level: Optional[int] = Field(default=None)

# User model
class User(SQLModel, table=True):
    __tablename__ = "rusers"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(max_length=255, unique=True, index=True)
    hashed_password: str = Field(max_length=255)
    role_id: Optional[int] = Field(default=None, foreign_key="roles.id")

    role: Optional[Role] = Relationship(back_populates="users")
    favourites: List["Favourites"] = Relationship(back_populates="user")




#-------- made by joyael----------

# # Product model
# class Product(Base):
#     __tablename__ = "products"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(255), unique=True, index=True)
#     tag = Column(String(255), index=True)
#     price = Column(Numeric(10, 2), index=True)



# Product model
class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field(max_length=255, unique=True, index=True)
    tag: str = Field(max_length=255, index=True)
    price: float = Field(default=None, index=True)  # Use float for Numeric(10, 2)

    favourites: List["Favourites"] = Relationship(back_populates="product")


# #favourites 
# class Favourites(Base):
#     __tablename__ = "favourites"

#     id = Column(Integer, primary_key=True, index=True)
#     user_id = Column(Integer, ForeignKey('rusers.id'))
#     product_id = Column(Integer, ForeignKey('products.id'))

# Favourites model
class Favourites(SQLModel, table=True):
    __tablename__ = "favourites"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    user_id: int = Field(foreign_key="rusers.id", index=True)
    product_id: int = Field(foreign_key="products.id", index=True)

    # Optional relationships if you want to access related data
    user: Optional["User"] = Relationship(back_populates="favourites")
    product: Optional["Product"] = Relationship(back_populates="favourites")


class Permission(SQLModel, table=True):
    __tablename__ = "permissions"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=255, unique=True)
    level: int = Field()  # Level required for this permission