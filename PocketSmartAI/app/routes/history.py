import json
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user
from app.models import RecommendationHistory, User
router=APIRouter()
@router.get("/history")
def history(user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    rows=db.query(RecommendationHistory).filter(RecommendationHistory.user_id==user.id).order_by(RecommendationHistory.created_at.desc()).all()
    return [{"id":r.id,"planner_type":r.planner_type,"created_at":r.created_at.isoformat(),"title":json.loads(r.result_json).get("title",r.planner_type.title())} for r in rows]
@router.get("/recommendations-details/{history_id}")
def recommendation_details(history_id:int,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    row=db.query(RecommendationHistory).filter(RecommendationHistory.id==history_id,RecommendationHistory.user_id==user.id).first()
    if not row: raise HTTPException(404,"Recommendation not found")
    result=json.loads(row.result_json);result["history_id"]=row.id;return result
