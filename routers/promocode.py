from fastapi import APIRouter, Response
from fastapi import APIRouter, Depends, HTTPException, Request, WebSocket, WebSocketDisconnect, status
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from auth.database import get_async_session
from dto import dto as DTO
from models.models import *

promoRouter = APIRouter()
promo_state = {}

@promoRouter.post('/add')
async def add_promo(promo: DTO.Promo, session: AsyncSession = Depends(get_async_session)):
    try:
        stmt = insert(Promo).values(promo.model_dump())
        await session.execute(stmt)
        await session.commit()
        promo_state[promo.code] = promo
        return "success"
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@promoRouter.get('/{promo}')
async def get_promo(promo: str, session: AsyncSession = Depends(get_async_session)) -> None:
    try:
        if promo in promo_state:
            return promo_state[promo]
        else:
            query = select(Promo).where(Promo.code == promo)
            result = await session.execute(query)
            data = result.mappings().first()
            return data
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@promoRouter.get('/{promo}/set')
async def set_promo(totalPrice: float, promo: str, session: AsyncSession = Depends(get_async_session)) -> None:
    try:
        if promo in promo_state:
            discount = 0
            if promo_state[promo].isPercent:
                x = totalPrice / 100 * promo_state[promo].discount
                discount = totalPrice - x
            else:
                discount = totalPrice - promo_state[promo].discount
            return discount
        else:
            query = select(Promo).where(Promo.code == promo)
            result = await session.execute(query)
            data = result.mappings().first()
            return data
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
