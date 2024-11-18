from fastapi import APIRouter, FastAPI
from login.routes import login_routes
app = FastAPI()

app.include_router(login_routes.router, tags=["Home"])

