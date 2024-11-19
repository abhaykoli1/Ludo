from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
import json
from login.model.login_model import LoginBody, LoginTable
router = APIRouter()


templates = Jinja2Templates(directory="templates")

@router.get("/")
async def landingPage(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})

@router.get("/login")
async def loginRoute(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})

@router.get("/signup")
async def loginRoute(request: Request):
    return templates.TemplateResponse('signup.html', {"request": request})

@router.post("/api/user/create")
async def create_user(body: LoginBody):
    findata = LoginTable.objects.get(email=body.email)
    if findata:
        return {
            "message": "user already exist",
            "data": None,
            "status": False
        }
    else:
        saveData = LoginTable(**body.dict())
        saveData.save()
        tojson = saveData.to_json()
        fromjson = json.loads(tojson)
        return {
            "message": "User Created Succes",
            "data": fromjson,
            "status": True
        }
