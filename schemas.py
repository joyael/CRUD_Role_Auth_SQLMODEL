from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    role_id: int  # Role ID to assign during registration

class User(BaseModel):
    id: int
    username: str
    role_id: int

    class Config:
        from_attributes = True
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token:str

class Role(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True
        orm_mode = True

#------added----------
class Product(BaseModel):
    id: int
    name: str
    tag:str
    price:float

    class Config:
        from_attributes = True
        orm_mode = True

class ProductCreate(BaseModel):
    name: str
    tag:str
    price:float


class ProductUpdate(BaseModel):
    product_name: str
    price: float

class ProductDelete(BaseModel):
    product_name: str

class Favourites(BaseModel):
    id: int
    name: str
    tag:str
    price:float

    class Config:
        from_attributes = True
        orm_mode = True

class FavouriteAdd(BaseModel):
    product_name: str

class FavouriteDelete(BaseModel):
    product_name: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str



