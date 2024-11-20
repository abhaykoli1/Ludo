from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
from login.model.login_model import LoginBody, LoginTable
router = APIRouter()

class LoginBodyLogin(BaseModel):
    email : str
    password: str




@router.post("/api/user/create")
async def create_user(body: LoginBody):
    findata = LoginTable.objects(email=body.email).first()
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


@router.post("/api/user/create")
async def create_user(body: LoginBody):
    findata = LoginTable.objects(email=body.email).first()
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

@router.get("/api/user/get-users")
async def get_User():
    findata = LoginTable.objects.all()
    tojson = findata.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "Here is all users",
        "data": fromjson,
        "status": True
    }

@router.post("/api/user/login")
async def login_user(body: LoginBodyLogin):
    findUser = LoginTable.objects(email=body.email).first()
    if findUser:
        if findUser.password == body.password:
            tojson = findUser.to_json()
            fromjson = json.loads(tojson)
            return {
                "message": "User Login Suces",
                "data":fromjson,
                "status": True
            }
        else:
            return {
                "message": "User password Inccorect",
                "data": None,
                "status": False
            }
    else:
        return {
                "message": "User not found",
                "data": None,
                "status": False
            }