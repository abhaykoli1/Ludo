from fastapi import APIRouter, FastAPI
from mongoengine import connect
from login.routes import login_routes
from ludoboard.routes import game_routes
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
connect(db="LudoBuddy",  host="mongodb+srv://hdark6336:a1s2d3f4g5h6j7k8l9@cluster0.kj9fw.mongodb.net/LudoBuddy")
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(login_routes.router, tags=["Home"])
app.include_router(game_routes.router, tags=["Game"])
