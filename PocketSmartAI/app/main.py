from pathlib import Path
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.config import settings
from app.database import init_db
from app.routes import auth, planners, session, history
BASE_DIR=Path(__file__).resolve().parent
app=FastAPI(title=settings.app_name,version="1.0.0")
app.add_middleware(CORSMiddleware,allow_origins=settings.cors_origin_list,allow_credentials=True,allow_methods=["*"],allow_headers=["*"])
app.mount("/static",StaticFiles(directory=BASE_DIR/"static"),name="static")
templates=Jinja2Templates(directory=str(BASE_DIR/"templates"))
@app.on_event("startup")
def startup(): init_db()
@app.get("/",response_class=HTMLResponse)
def index(request:Request): return templates.TemplateResponse("index.html",{"request":request})
for path,template in [("/login","login.html"),("/register","register.html"),("/dashboard","dashboard.html"),("/planner/home","home_planner.html"),("/planner/party","party_planner.html"),("/planner/jewelry","jewelry_planner.html"),("/history","history.html")]:
    def page(request:Request,_template=template): return templates.TemplateResponse(_template,{"request":request})
    app.get(path,response_class=HTMLResponse)(page)
@app.get("/recommendations/{history_id}",response_class=HTMLResponse)
def recommendations(request:Request,history_id:int): return templates.TemplateResponse("recommendations.html",{"request":request,"history_id":history_id})
@app.get("/health")
def health(): return {"status":"ok","service":settings.app_name}
@app.get("/startup")
def startup_status(): return {"status":"ready","ai_enabled":bool(settings.gemini_api_key and settings.ai_enabled),"model":settings.gemini_model}
app.include_router(auth.router);app.include_router(planners.router);app.include_router(session.router);app.include_router(history.router)
