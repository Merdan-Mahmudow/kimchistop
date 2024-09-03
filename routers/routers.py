import json
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from routers.category import categoryRouter
from routers.food import foodRouter
from routers.user import userRouter
from routers.order import orderRouter
from routers.payment import payment_router
from routers.promocode import promoRouter

from yookassa import Configuration, Payment
import uuid

Configuration.account_id = "393161"
Configuration.secret_key = "test_zaHD1EDc8Mi2f_LK0evUH5neTKsKdhGs3CyacbObQ54"
templates = Jinja2Templates(directory="./templates")

router = APIRouter()


@router.get('/')
async def main_app(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@router.get('/manager')
async def manager(request: Request):
    return templates.TemplateResponse("manager.html", {"request": request})


# @router.on_event("startup")
# async def startup():
#     with open('user_state.json', 'r') as f:
#         global user_state
#         user_state = json.load(f)

router.include_router(userRouter, prefix="/user", tags=["Пользователи"])
router.include_router(foodRouter, prefix="/food", tags=["Еда"])
router.include_router(categoryRouter, prefix='/category', tags=["Категории"])
router.include_router(orderRouter, prefix='/order', tags=["Заказы"])
router.include_router(payment_router, prefix='/payments', tags=["Оплата"])
router.include_router(promoRouter, prefix='/promocode', tags=["Промокоды"])