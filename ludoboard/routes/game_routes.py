from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from fastapi.staticfiles import StaticFiles

router = APIRouter()
templates = Jinja2Templates(directory="templates")
@router.get("/4player")
async def player4(request: Request):
    return templates.TemplateResponse('4player.html', {"request": request})
