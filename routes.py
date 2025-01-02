from fastapi import APIRouter, Depends, HTTPException, status, Query
# from sqlalchemy.orm import Session
from sqlalchemy import and_
from sqlmodel import Session
from database import get_db
from auth import hash_password, create_access_token, verify_password, create_refresh_token, verify_refresh_token

from models import User as UserModel, Role as RoleModel, Product as ProductModel, Favourites as FavouritesModel
from schemas import UserCreate, User, Token, Role, Product, ProductCreate, ProductUpdate, ProductDelete, FavouriteAdd, FavouriteDelete, RefreshTokenRequest

from user_role import get_current_user, role_required
from typing import List, Dict

router = APIRouter()

# User registration
@router.post("/roleauth/register", response_model=User )
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = UserModel(username=user.username, hashed_password=hashed_password, role_id=user.role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# User login
@router.post("/roleauth/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.username})
    refresh_token = create_refresh_token(data={"sub":db_user.username})
    return {"access_token": access_token, "token_type": "bearer", "refresh_token":refresh_token}

# Get all roles
@router.get("/roleauth/roles", response_model=list[Role], dependencies=[Depends(role_required("owner"))])
def get_roles(db: Session = Depends(get_db)):
    return db.query(RoleModel).all()

# Admin-only route
@router.get("/roleauth/admin", dependencies=[Depends(role_required(["admin",]))])
def read_admin_data():
    return {"message": "Welcome, Admin!"}

# Owner-only route
@router.get("/roleauth/owner", dependencies=[Depends(role_required(["owner",]))])
def read_owner_data():
    return {"message": "Welcome, Owner!"}

# User group 1 route
@router.get("/roleauth/user-group-1", dependencies=[Depends(role_required(["user group 1",]))])
def read_user_group_1_data():
    return {"message": "Welcome, User Group 1!"}

# User group 2 route
@router.get("/roleauth/user-group-2", dependencies=[Depends(role_required(["user group 2",]))])
def read_user_group_2_data():
    return {"message": "Welcome, User Group 2!"}



# admin insert update
# owner delete 
# user view


#inserting route
@router.post("/roleauth/products/insert", response_model=Product, dependencies=[Depends(role_required(["admin","owner"]))])
def insert_product(product : ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductModel(name = product.name,tag = product.tag,price = product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


#displaying route
@router.get("/roleauth/products/viewall", response_model=List[Product], dependencies=[Depends(role_required(["admin","owner","user group 1","user group 2"]))])
def display_products(db: Session = Depends(get_db)):
    return db.query(ProductModel).all()


#display with condition
@router.get("/roleauth/products/view", response_model=list[Product], 
                                        dependencies=[Depends(role_required(["admin", "owner", "user group 1", "user group 2"]))])
def display_products_below_price_limit(price_limit: float = Query(..., description="Price limit for filtering products"), 
                    db: Session = Depends(get_db)):
    # Query the database for products with a price less than the price limit
    products = db.query(ProductModel).filter(ProductModel.price < price_limit).all()
    return products


#updating route for admin
@router.post("/roleauth/products/update", response_model=Product, 
                                        dependencies=[Depends(role_required(["admin", "owner"]))])
def update_product(product_update: ProductUpdate, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.name == product_update.product_name).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found.")
    db_product.price = product_update.price
    db.commit()
    db.refresh(db_product)
    return db_product  # Return the updated product



#deleting route for owner
@router.delete("/roleauth/products/delete", response_model=Product, 
                                        dependencies=[Depends(role_required(["owner",]))])
def delete_product(product_delete: ProductDelete, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.name == product_delete.product_name).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found.")
    db.delete(db_product)
    db.commit()
    return db_product


#adding favourites
@router.post("/roleauth/favourites/add", 
                                        dependencies=[Depends(role_required(["user group 1","user group 2"]))])
def add_favourite(favourite_add:FavouriteAdd, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_product = db.query(ProductModel).filter(ProductModel.name == favourite_add.product_name).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found.")
    
    db_favourite = db.query(FavouritesModel).filter(
        and_(
            FavouritesModel.product_id == db_product.id,
            FavouritesModel.user_id == current_user.id
        )
    ).first()
    if db_favourite:
        raise HTTPException(status_code=405, detail="Product already added to favourites")
    else:
        db_favourite = FavouritesModel(user_id=current_user.id, product_id=db_product.id)
        db.add(db_favourite)
        db.commit()
        db.refresh(db_favourite)
    return {"id":db_favourite.id, "product_name" : db_product.name, "user_name" : current_user.username}

#deleting favourites
@router.delete("/roleauth/favourites/delete",
                                        dependencies=[Depends(role_required(["user group 1","user group 2"]))])
def delete_favourite(favourite_delete:FavouriteDelete, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    db_product = db.query(ProductModel).filter(ProductModel.name == favourite_delete.product_name).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found.")
    
    db_favourite = db.query(FavouritesModel).filter(
        and_(
            FavouritesModel.product_id == db_product.id,
            FavouritesModel.user_id == current_user.id
        )
    ).first()
    if not db_favourite:
        raise HTTPException(status_code=404, detail="Product not in favourites")
    else:
        db.delete(db_favourite)
        db.commit()
    return {"id":db_favourite.id, "product_name" : db_product.name, "user_name" : current_user.username}


@router.get("/roleauth/favourites/view",
            dependencies=[Depends(role_required(["user group 1", "user group 2"]))])
def view_favourites(db: Session = Depends(get_db), current_user = Depends(get_current_user)) -> List[Dict]:
    db_favourites = db.query(FavouritesModel).filter(FavouritesModel.user_id == current_user.id).all()
    
    if not db_favourites:
        raise HTTPException(status_code=404, detail="No favourites found.")
    
    favourites_result = []
    
    for favourite in db_favourites:
        temp = {}
        db_product = db.query(ProductModel).filter(ProductModel.id == favourite.product_id).first()
        pd_name = db_product.name if db_product else "Don't Exist"
        
        temp["id"] = favourite.id
        temp["product_name"] = pd_name
        favourites_result.append(temp)
    
    return favourites_result
   

# Refresh endpoint
@router.post("/roleauth/refresh")
async def refresh_token(request: RefreshTokenRequest):
    # Verify the refresh token
    payload = verify_refresh_token(request.refresh_token)
    # Create a new access token using the username from the payload
    new_access_token = create_access_token(data={"sub": payload["sub"]}, refresh=True, refresh_token=request.refresh_token)
    return {"access_token": new_access_token, "token_type": "bearer"}