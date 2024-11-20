from fastapi import APIRouter, Request, Depends
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import json
from login.model.login_model import LoginBody, LoginTable
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

class LoginBodyLogin(BaseModel):
    email : str
    password: str


# OAuth Configuration
config = Config(".env")  # Create a .env file with CLIENT_ID and CLIENT_SECRET
oauth = OAuth(config)
oauth.register(
    name="google",
    client_id=config("GOOGLE_CLIENT_ID"),
    client_secret=config("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

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
async def login_user(request: Request, body: LoginBodyLogin):
    findUser = LoginTable.objects(email=body.email).first()
    if findUser:
        if findUser.password == body.password:
            tojson = findUser.to_json()
            fromjson = json.loads(tojson)
            request.session["user"] = {
                "data":fromjson,
            }
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

@router.get("/auth/google")
async def google_login(request: Request):
    redirect_uri = request.url_for("auth")  # The callback URL
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/callback")
async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)
    user = token.get("userinfo")  # Get user info
    email = user["email"]
    finduser = LoginTable.objects(email=email).first()
    print(user)
    print(finduser)
    if finduser:
        # You can store user info in your database here
        tojson = finduser.to_json()
        fromjson = json.loads(tojson)
        request.session["user"] = {
            "data":fromjson,
        }
        return RedirectResponse(url="/home")
    else:
        saveUserData = LoginTable(email=user['email'], name=user['name'], password=user['iat'])
        saveUserData.save()
        tojson = saveUserData.to_json()
        fromjson = json.loads(tojson)
        request.session["user"] = {
            "data":fromjson,
        }
        return RedirectResponse(url="/home")

    return {"error": "Unable to authenticate user"}