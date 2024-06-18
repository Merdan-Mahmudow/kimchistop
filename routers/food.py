import json
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from auth.database import get_async_session
from dto import dto as DTO
from models.models import *
from typing import Any, Optional

foodRouter = APIRouter()

@foodRouter.post("/")
async def food_add(foodName: str, price: int, description: str, image: str, category: int, foodDTO: DTO.Food, session: AsyncSession = Depends(get_async_session)):
    try:
        query = insert(Food).values(foodName=foodName, price=price, description=description, image=image, category=category)
        await session.execute(query)
        await session.commit()
        return {"message": "Food added successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@foodRouter.get("/")
async def food_get(category: int | None = None, session: AsyncSession = Depends(get_async_session)):
    try:
        if category is None:
            query = select(Food)
        else:
            query = select(Food).where(Food.category == category)
        result = await session.execute(query)
        data = result.mappings().all()
        datas = []
        for i in range(len(data)):
            datas.append(data[i]["Food"])
        return datas
    except Exception as e:
        if not data:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No food found") 
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@foodRouter.get("/{id}")
async def food_search_by_id(id: int, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Food).where(Food.id == id)
        result = await session.execute(query)
        food = result.mappings().all()         
        return food[0]["Food"]
    except Exception as e:
        if not food:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@foodRouter.get("/search/{name}")
async def food_search_by_name(name: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(Food).where(Food.foodName == name)
        result = await session.execute(query)
        found = result.mappings().all()
        
        return found[0]["Food"]
    except Exception as e:
        if not found:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@foodRouter.delete("/{id}")
async def food_del(id: int, foodDTO: DTO.Food, session: AsyncSession = Depends(get_async_session)):
    try:
        query = delete(Food).where(Food.id == id)
        await session.execute(query)
        await session.commit()
        return {"message": "Food deleted successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@foodRouter.patch("/{id}")
async def food_update(id: int = None, foodName: str = None, price: int = None, image: str = None, description: str = None, category: int = None, session: AsyncSession = Depends(get_async_session)):
    try:
        query = update(Food).where(Food.id == id).values(foodName=foodName, price=price, description=description, image=image, category=category)
        await session.execute(query)
        await session.commit()
        return {"message": "Food updated successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
