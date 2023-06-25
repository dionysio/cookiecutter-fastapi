from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates

router = APIRouter()


@router.get("/")
async def index(request: Request):
    templates = Jinja2Templates("templates")
    return templates.TemplateResponse(
        "root.html",
        context={"request": request},
    )
