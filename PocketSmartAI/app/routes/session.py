from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.models import User
router=APIRouter()
@router.get("/session-info")
def session_info(user:User=Depends(get_current_user)): return {"logged_in":True,"user_id":user.id,"name":user.name,"email":user.email}
@router.get("/session-data")
def session_data(user:User=Depends(get_current_user)):
    recent=sorted(user.recommendations,key=lambda x:x.created_at,reverse=True)[:5]
    return {"user_id":user.id,"recommendation_count":len(user.recommendations),"recent_planners":[r.planner_type for r in recent]}
