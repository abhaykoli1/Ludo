from fastapi import APIRouter, FastAPI
from mongoengine import connect
from login.routes import login_routes
from ludoboard.routes import game_routes
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.templating import Jinja2Templates
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.middleware.sessions import SessionMiddleware
import os
from dotenv import load_dotenv
from starlette.staticfiles import StaticFiles
from passbook.routes import passbook_routes
from wallet.wallet_model import WalletTable
from bson import ObjectId
import json

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")


# If SECRET_KEY is not found, raise an error
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not found in .env file")
else:
    print("found" + SECRET_KEY)
    
connect('LudoTest', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/LudoTest")
app = FastAPI()
app.add_middleware(
    SessionMiddleware,
    secret_key=SECRET_KEY,
    max_age=3600,
    session_cookie="your_session_cookie",
)
config = Config(".env")  # Create a .env file with CLIENT_ID and CLIENT_SECRET
oauth = OAuth(config)
oauth.register(
    name="google",
    client_id=config("GOOGLE_CLIENT_ID"),
    client_secret=config("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(login_routes.router, tags=["Home"])
app.include_router(game_routes.router, tags=["Game"])
app.include_router(passbook_routes.router, tags=["payments"])

# page Routes
@app.get("/")
async def landingPage(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})


@app.get("/login")
async def loginRoute(request: Request):
    return templates.TemplateResponse('login.html', {"request": request})

@app.get("/signup")
async def loginRoute(request: Request):
    return templates.TemplateResponse('signup.html', {"request": request})

@app.get("/game")
async def landingPage(request: Request):
    return templates.TemplateResponse('ludo_4player.html', {"request": request})
@app.get("/deposit")
async def landingPage(request: Request):
    return templates.TemplateResponse('deposit.html', {"request": request})
@app.get("/home")
async def landingPage(request: Request):
    user= request.session.get("user")
    wallet = WalletTable.objects.get(userid=str(user["data"]["_id"]["\u0024oid"]))
    wallettojson = wallet.to_json()
    walletFromjson = json.loads(wallettojson)
    data = {
        "user": user,
        "wallet": walletFromjson
    }
    print(data)
    return templates.TemplateResponse('home.html', {"request": request, **data})