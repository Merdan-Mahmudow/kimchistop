import asyncio
import json
from websockets.sync.client import connect
from fastapi import APIRouter, Depends, HTTPException, Request, WebSocket, WebSocketDisconnect, status
from fastapi.templating import Jinja2Templates
import requests
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from auth.database import get_async_session
from dto import dto as DTO
from models.models import *
import random
from .payment import currentPayment

templates = Jinja2Templates(directory="./templates")

orderRouter = APIRouter()
TOKEN = '6937107637:AAFarU8swL-mp7oLC0sMz44A7-F3q0QuD4Y'
ADMIN_TOKEN = "7141464443:AAHslp-j0q3rHKMzk-CAaSi0T8LkVdI2kus"

def generate_order_id():
    """Generates a unique order ID."""
    return random.randint(10000000, 99999999)

@orderRouter.post("/")
async def order_add(orederDTO: DTO.Order, chatID: int | None = None, session: AsyncSession = Depends(get_async_session)):
    try:
        async with session:
            query = insert(Order).values(orederDTO.model_dump())
            await session.execute(query)
            await session.commit()
            orderItems = orederDTO.items

            admin_query = select(User.chatID).where(User.role == "admin")
            result = await session.execute(admin_query)
            admin_chatID = result.mappings().all()
            admins = [admin['chatID'] for admin in admin_chatID]
            
                
            
            isDelivery = ""
            if orederDTO.isDelivery:
                isDelivery = "ДОСТАВКА"
            else:
                isDelivery = "САМОВЫВОЗ"
            # text_for_send = f"Спасибо за заказ!\n\nВаш заказ №{order_id} в обработке.\n Будет готов через 18 минут.\n\nОплата: {orederDTO.payment}\n\n❗ЗАБРАТЬ САМОСТОЯТЕЛЬНО❗\n\n📍Адрес: {orederDTO.address}\n\nЗаказ:\n{"".join([f"{item['count']} - {item['foodName']} - {item['price']} руб." for item in orderItems])}\n"
            text_for_send = f"Спасибо за заказ!\n\nВаш заказ №{orederDTO.number} в обработке.\nБудет готов через 18 минут.\n\nОплата: {orederDTO.payment}\n\n❗ЗАБРАТЬ САМОСТОЯТЕЛЬНО❗\n\n📍Адрес: {str(orederDTO.address)}\n\nЗаказ:\n" + "".join([f"{item['count']}   x   {item['foodName']}    {item['price']} руб.\n" for item in orderItems]) + f"\n{orederDTO.cutlery}  x  Приборов" + f"\n\nИтого: {orederDTO.total}\n\n💮🍜"
            text_for_send_admin = f"Новый заказ №{orederDTO.number}\n\nОплата: {orederDTO.payment}\n\nСпособ получения: {isDelivery}\n\n📍Адрес: {str(orederDTO.address)}\n\nЗаказ:\n" + "".join([f"{item['count']}   x   {item['foodName']}    {item['price']} руб.\n" for item in orderItems]) + f"\n{orederDTO.cutlery}  x  Приборов" + f"\n\nИтого: {orederDTO.total}"
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chatID}&text={text_for_send}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@orderRouter.get("/")
async def order_get(session: AsyncSession = Depends(get_async_session)):
    try:
        async with session:
            query = select(Order)
            result = await session.execute(query)
            data = result.scalars().all()
            return data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@orderRouter.post("/manage")
async def orders_manage():
    pass
    
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []
    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
            print(connection)


manager = ConnectionManager()
@orderRouter.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await manager.connect(websocket)
    try:
        while True:
            global currentPayment
            data = await websocket.receive_text()
            print(data)
            await manager.broadcast(f'[{data},'.join(json.dumps(currentPayment)) + ']')
            print(currentPayment)
            currentPayment = {}
    except WebSocketDisconnect:
        await manager.disconnect(websocket)