from fastapi import APIRouter, FastAPI
from mongoengine import connect
from login.routes import login_routes

from ludoboard.routes import game_routes
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
connect('LudoTest', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/LudoTest")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)
from starlette.staticfiles import StaticFiles
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(login_routes.router, tags=["Home"])
app.include_router(game_routes.router, tags=["Game"])


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
@app.get("/home")
async def landingPage(request: Request):
    return templates.TemplateResponse('home.html', {"request": request})