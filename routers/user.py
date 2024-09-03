# import json
# from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
# from sqlalchemy import delete, insert, select, update
# from sqlalchemy.ext.asyncio import AsyncSession
# from auth.database import get_async_session
# from dto import dto as DTO
# from models.models import *
# from typing import Any, Optional


# userRouter = APIRouter()

# @userRouter.get('/{nickname}')
# async def user_get(nickname: str, session: AsyncSession = Depends(get_async_session)):
#     query = select(User).where(User.nickname == nickname)
#     result = await session.execute(query)
#     data = result.mappings().all()
#     if data == []:
#         return 404
#     else:
#         return data[0]["User"]

# @userRouter.post('/')
# async def user_add(userDTO: DTO.User,session: AsyncSession = Depends(get_async_session)):
#     query = insert(User).values(userDTO.model_dump())
#     print(query)
#     await session.execute(query)
#     await session.commit()
#     return {
#         "message": "User added successfully"
#     }

# @userRouter.patch('/{nickname}')
# async def user_patch(nickname: str, userDTO: DTO.User, session: AsyncSession = Depends(get_async_session)):
#     # query = update(User.name).where(User.nickname == nickname).values(userDTO.name)
#     query = update(User).where(User.nickname == nickname).values(name=userDTO.name)
#     print(query)
#     await session.execute(query)
#     await session.commit()
#     await session.commit()

# @userRouter.get('/{nickname}/fav')
# async def get_favourites(nickname: str, session: AsyncSession = Depends(get_async_session)):
#     query = select(User.favourites).where(User.nickname == nickname)
#     result = await session.execute(query)
#     return result.mappings().all()
import asyncio
import json
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from auth.database import get_async_session
from dto import dto as DTO
from models.models import *
# from .routers import user_state as us
import requests

userRouter = APIRouter()

def isNull(value):
  """
  Checks if a value is null or not.

  Args:
    value: The value to check.

  Returns:
    True if the value is null, False otherwise.
  """
  return value is None

# State dictionary to store user objects
user_state = {}



@userRouter.post('/setstate')
async def user_get(nickname: str, session: AsyncSession = Depends(get_async_session)):
    try:
        # Check if user is already in state
        if nickname in user_state:
            return "User already in state"

        # Fetch user from database
        query = select(User).where(User.nickname == nickname)
        result = await session.execute(query)
        data = result.mappings().all()
        # Store user in state
        user_state[nickname] = data[0]["User"]
        for i in range(len(user_state[nickname].favourites)):
            user_state[nickname].favourites[i] = int(user_state[nickname].favourites[i])

        return "User added to state"
    except Exception as e:
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@userRouter.get('/{nickname}')
async def user_get(nickname: str, session: AsyncSession = Depends(get_async_session)):
    try:
        # Check if user is already in state
        if nickname in user_state:
            return user_state[nickname]

        # Fetch user from database
        query = select(User).where(User.nickname == nickname)
        result = await session.execute(query)
        data = result.mappings().all()
        # Store user in state
        user_state[nickname] = data[0]["User"]
        print(user_state[nickname])
        for i in range(len(user_state[nickname].favourites)):
            user_state[nickname].favourites[i] = int(user_state[nickname].favourites[i])

        return user_state[nickname]
    except Exception as e:
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

@userRouter.post('/')
async def user_add(userDTO: DTO.User, session: AsyncSession = Depends(get_async_session)):
    try:
        # Insert user into database
        query = insert(User).values(userDTO.model_dump())
        await session.execute(query)
        await session.commit()

        # Add user to state
        user_state[userDTO.nickname] = userDTO

        return {"message": "User added successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@userRouter.patch('/{nickname}')
async def user_patch(nickname: str, userDTO: DTO.User, session: AsyncSession = Depends(get_async_session)):
    try:
        # Update user in database
        query = update(User).where(User.nickname == nickname).values(favourites=userDTO.favourites)
        await session.execute(query)
        await session.commit()

        # Update user in state
        if nickname in user_state:
            user_state[nickname].name = userDTO.name

        return {"message": "User updated successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@userRouter.get('/{nickname}/fav')
async def get_favourites(nickname: str, session: AsyncSession = Depends(get_async_session)):
    try:
        foods = []
        if user_state[nickname].favourites is None:
            return foods
        for i in range(len(user_state[nickname].favourites)):
            print(user_state[nickname].favourites[i])
            query = select(Food).where(Food.id == user_state[nickname].favourites[i])
            result = await session.execute(query)
            data = result.mappings().first()
            food = data["Food"]
            foods.append(food)
        return foods
    except Exception as e:
        if nickname not in user_state:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@userRouter.patch('/{nickname}/fav')
async def add_favourite(nickname: str, favourite_item: int, session: AsyncSession = Depends(get_async_session)):
    try:
        fav = user_state[nickname].favourites
        if favourite_item in fav:
            fav.remove(favourite_item)
        else:
            fav.append(favourite_item)

        # # Update user in database
        query = update(User).where(User.nickname == nickname).values(favourites=fav)
        await session.execute(query)
        await session.commit()
        foods = []
        for i in range(len(fav)):
            query = select(Food).where(Food.id == fav[i])
            result = await session.execute(query)
            data = result.mappings().first()
            food = data["Food"]
            foods.append(food)
        return foods
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@userRouter.delete('/{nickname}')
async def user_delete(nickname: str, session: AsyncSession = Depends(get_async_session)):
    try:
        # Delete user from database
        query = delete(User).where(User.nickname == nickname)
        await session.execute(query)
        await session.commit()

        # Remove user from state
        if nickname in user_state:
            del user_state[nickname]

        return {"message": "User deleted successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
@userRouter.patch('/role/{nickname}')
async def user_role(nickname: str, role: str, session: AsyncSession = Depends(get_async_session)):
    try:
        # Update user in database
        query = update(User).where(User.nickname == nickname).values(role=role)
        await session.execute(query)
        await session.commit()

        # Update user in state
        if nickname in user_state:
            user_state[nickname].role = role
        return {"message": "User role updated successfully"}
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

