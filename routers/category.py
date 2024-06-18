import json
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from auth.database import get_async_session
from dto import dto as DTO
from models.models import *
from typing import Any, Optional


categoryRouter = APIRouter()


@categoryRouter.post('/')
async def category_add(catDTO: DTO.Category, session: AsyncSession = Depends(get_async_session)):
    query = insert(Category).values(catDTO.model_dump())
    await session.execute(query)
    await session.commit()

@categoryRouter.get('/')
async def category_name_get(session: AsyncSession = Depends(get_async_session)):
    query = select(Category.categoryName)
    result = await session.execute(query)    
    return result.mappings().all()

@categoryRouter.get('/all')
async def category_all_get(session: AsyncSession = Depends(get_async_session)):
    query = select(Category)
    result = await session.execute(query)
    return result.mappings().all()

@categoryRouter.patch('/foods/{id}')
async def update_categories(id: int, catDTO: DTO.Category, session: AsyncSession = Depends(get_async_session)):
    query = update(Category).where(Category.id == id).values(food=catDTO.food)
    await session.execute(query)
    await session.commit()
    return "success"

@categoryRouter.patch('/{id}')
async def update_category_name(id: int, name: str, session: AsyncSession = Depends(get_async_session)):
    query = update(Category).where(Category.id == id).values(categoryName = name)
    await session.execute(query)
    await session.commit()
    return "success"

@categoryRouter.get('/dis')
async def distributing_foods(session: AsyncSession = Depends(get_async_session)):
    query_food_id = select(Food.id)
    query_food = select(Food)
    query_cat_name = select(Category.categoryName)
    query_cat_foods = select(Category.food)


    result_food_id = await session.execute(query_food_id)
    result_food = await session.execute(query_food)
    result_cat_name = await session.execute(query_cat_name)
    result_cat_food = await session.execute(query_cat_foods)


    cat_name = result_cat_name.mappings().all()
    cat_foods = result_cat_food.mappings().all()
    food_id = result_food_id.mappings().all()
    foods = result_food.mappings().all()

    result = []

    for el in range(len(cat_name)):
        result.append({
            "categoryName": cat_name[el]["categoryName"],
            "foods": []
        })
        for e in range(len(food_id)):
            if food_id[e]["id"] in cat_foods[el]["food"]:
                result[el]["foods"].append(foods[e]["Food"])
    return result