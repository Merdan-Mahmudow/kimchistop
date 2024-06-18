import json
from fastapi import APIRouter, Depends, HTTPException, status
import requests
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from auth.database import get_async_session
from dto import dto as DTO
from models.models import *
import random

orderRouter = APIRouter()
TOKEN = '6937107637:AAFarU8swL-mp7oLC0sMz44A7-F3q0QuD4Y'

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
                
            # text_for_send = f"Спасибо за заказ!\n\nВаш заказ №{order_id} в обработке.\n Будет готов через 18 минут.\n\nОплата: {orederDTO.payment}\n\n❗ЗАБРАТЬ САМОСТОЯТЕЛЬНО❗\n\n📍Адрес: {orederDTO.address}\n\nЗаказ:\n{"".join([f"{item['count']} - {item['foodName']} - {item['price']} руб." for item in orderItems])}\n"
            text_for_send = f"Спасибо за заказ!\n\nВаш заказ №{orederDTO.number} в обработке.\nБудет готов через 18 минут.\n\nОплата: {orederDTO.payment}\n\n❗ЗАБРАТЬ САМОСТОЯТЕЛЬНО❗\n\n📍Адрес: {str(orederDTO.address)}\n\nЗаказ:\n" + "".join([f"{item['count']}   x   {item['foodName']}    {item['price']} руб.\n" for item in orderItems]) + f"\n\nИтого: {orederDTO.total}\n\n💮🍜"
            requests.get(f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chatID}&text={text_for_send}")
            return {"message": "Order added successfully"}
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
