import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.routers import *
from starlette.responses import FileResponse 
app = FastAPI(tags=["Freestyle BOT"])

origins = [
    "http://localhost:3000",
    "https://skyrodev.ru",
    "http://0.0.0.0:8000",
    "https://backend.skyrodev.ru",
    "http://127.0.0.1:3000",
    "https://kimchistop.ru",
    "https://api.kimchistop.ru"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


app.include_router(router)