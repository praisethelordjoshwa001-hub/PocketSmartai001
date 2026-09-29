import json
from pathlib import Path
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import RecommendationHistory, User
from app.schemas import HomeRequest, PartyRequest, RecommendationResponse
from app.services.recommendation_service import build_home, build_party, build_jewelry
from app.config import settings
router=APIRouter();Path("uploads").mkdir(exist_ok=True)
def _save(db,user,planner,payload,result):
    row=RecommendationHistory(user_id=user.id,planner_type=planner,input_json=json.dumps(payload,ensure_ascii=False),result_json=json.dumps(result,ensure_ascii=False));db.add(row);db.commit();db.refresh(row);result["history_id"]=row.id;return result
@router.post("/generate-home",response_model=RecommendationResponse)
def generate_home(payload:HomeRequest,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return _save(db,user,"home",payload.model_dump(),build_home(payload.model_dump()))
@router.post("/generate-party",response_model=RecommendationResponse)
def generate_party(payload:PartyRequest,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    return _save(db,user,"party",payload.model_dump(),build_party(payload.model_dump()))
@router.post("/generate-jewelry")
async def generate_jewelry(budget:float=Form(...),occasion:str=Form(...),style:str=Form("Elegant"),metal:str=Form("Any"),outfit_color:str=Form(""),notes:str=Form(""),outfit_image:UploadFile|None=File(None),user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    if budget<=0: raise HTTPException(422,"Budget must be greater than zero")
    image_bytes=None;mime=None
    if outfit_image:
        if outfit_image.content_type not in {"image/jpeg","image/png","image/webp"}: raise HTTPException(415,"Only JPEG, PNG or WEBP images are supported")
        image_bytes=await outfit_image.read();mime=outfit_image.content_type
        if len(image_bytes)>settings.max_upload_mb*1024*1024: raise HTTPException(413,f"Image must be <= {settings.max_upload_mb} MB")
    payload={"budget":budget,"occasion":occasion,"style":style,"metal":metal,"outfit_color":outfit_color,"notes":notes,"image_uploaded":bool(image_bytes)}
    return _save(db,user,"jewelry",payload,build_jewelry(payload,image_bytes,mime))
