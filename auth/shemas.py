from typing import Optional
from fastapi_users import schemas
from pydantic import ConfigDict, EmailStr
import pydantic_core


class UserRead(schemas.BaseUser[int]):
    bio: str
    phone: str
    client: bool
    role_id: int
    date: str
    descr: str
    listOfOrders: list
    rate: float
    comments: str
    avatar: str
    activeBalance: float
    frozenBalance: float
    transactions: str
    userStatus: str
    activeTasks: list
    implementer: bool
    pendingTasks: list

    email: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False


    model_config = ConfigDict(from_attributes=True)

class UserCreate(schemas.BaseUserCreate):
    bio: str
    phone: str
    client: bool
    role_id: int
    date: str
    descr: str
    listOfOrders: list
    rate: float
    comments: str
    avatar: str
    activeBalance: float
    frozenBalance: float
    transactions: str
    userStatus: str
    activeTasks: list
    implementer: bool
    pendingTasks: list

    email: str
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class UserUpdate(schemas.BaseUserUpdate):
    bio: Optional[str] = None
    resume: Optional[str] = None
    rate: Optional[float] = None
    comments: Optional[str] = None
    listOfOrders: Optional[str] = None
    avatar: Optional[str] = None
    activeBalance: Optional[float] = None
    frozenBalance: Optional[float] = None
    transactions: Optional[str] = None
    userStatus: Optional[str] = None
    password: Optional[str] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
    is_verified: Optional[bool] = None