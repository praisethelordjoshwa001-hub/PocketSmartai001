from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.auth import decode_access_token
from app.database import get_db
from app.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)

def get_current_user(request: Request, db: Session = Depends(get_db), token: str | None = Depends(oauth2_scheme)):
    token = token or request.cookies.get("access_token")
    if not token: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required")
    user_id = decode_access_token(token)
    user = db.get(User, user_id)
    if not user: raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user
