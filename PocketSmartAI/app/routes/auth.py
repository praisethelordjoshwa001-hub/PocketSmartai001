from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.schemas import RegisterRequest, LoginRequest, TokenResponse
from app.auth import hash_password, verify_password, create_access_token
router=APIRouter()
def _cookie(response,token): response.set_cookie("access_token",token,httponly=True,samesite="lax",secure=False,max_age=86400)
@router.post("/register")
def register(payload:RegisterRequest,response:Response,db:Session=Depends(get_db)):
    email=payload.email.lower()
    if db.query(User).filter(User.email==email).first(): raise HTTPException(409,"Email is already registered")
    user=User(email=email,name=payload.name.strip(),password_hash=hash_password(payload.password));db.add(user);db.commit();db.refresh(user)
    _cookie(response,create_access_token(user.id));return {"message":"Registration successful","user":{"id":user.id,"name":user.name,"email":user.email}}
@router.post("/login")
def login(payload:LoginRequest,response:Response,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==payload.email.lower()).first()
    if not user or not verify_password(payload.password,user.password_hash): raise HTTPException(401,"Invalid email or password")
    _cookie(response,create_access_token(user.id));return {"message":"Login successful","user":{"id":user.id,"name":user.name,"email":user.email}}
@router.post("/token",response_model=TokenResponse)
def token(payload:LoginRequest,response:Response,db:Session=Depends(get_db)):
    user=db.query(User).filter(User.email==payload.email.lower()).first()
    if not user or not verify_password(payload.password,user.password_hash): raise HTTPException(401,"Invalid email or password")
    access_token=create_access_token(user.id);_cookie(response,access_token);return {"access_token":access_token,"token_type":"bearer"}
@router.post("/logout")
def logout(response:Response): response.delete_cookie("access_token");return {"message":"Logged out"}
