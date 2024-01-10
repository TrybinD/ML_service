from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates

from service.api.security import get_current_user_from_cookie
from service.api.repositories.predictor_repo import PredictorRepository

router = APIRouter(prefix="", tags=["Pages"])

templates = Jinja2Templates(directory="src/service/front/templates")

@router.get("/auth")
def get_auth_page(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})

@router.get("/")
async def get_index_page(request: Request, 
                   user = Depends(get_current_user_from_cookie)):
    
    models = await PredictorRepository().find_by_options(is_active=True)

    return templates.TemplateResponse("index.html", {"request": request,
                                                     "user_name": user.username,
                                                     "models": models})