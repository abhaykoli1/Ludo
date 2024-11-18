from fastapi import APIRouter
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from starlette.requests import Request
router = APIRouter()


templates = Jinja2Templates(directory="templates")

@router.get("/")
async def landingPage(request: Request):
    return templates.TemplateResponse('index.html', {"request": request})