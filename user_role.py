from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from models import User,Permission  # Import your User model
from database import get_db  # Import your database session dependency
from auth import SECRET_KEY, ALGORITHM  # Import your secret key and algorithm
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/roleauth/login")

# Get current user
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user


# Role-based access control
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

def role_required(permission_name: str):
    def role_checker(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
        
        # Fetch the permission from the database
        permission = db.query(Permission).filter(Permission.name == permission_name).first()
        if permission is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

        # Check if the user's role level is sufficient
        if user.role.level > permission.level:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
        
        return user
    return role_checker