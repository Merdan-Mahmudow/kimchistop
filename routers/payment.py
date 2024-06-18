from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from yookassa import Payment
import uuid

payment_router = APIRouter()
templates = Jinja2Templates(directory="./templates")


@payment_router.post('/')
async def payment(request: Request ,amount: float, description: str):
    idempotence_key = str(uuid.uuid4())
    payment = Payment.create({
        "amount": {
            "value": str(amount),
            "currency": "RUB"
        },
        "confirmation": {
            "type": "embedded"
        },
        "capture": True,
        "description": description
    }, idempotence_key)

    # get confirmation url
    confirmation_token = payment.confirmation.confirmation_token


    return confirmation_token



@payment_router.get('/')
async def payments_list(amount: float, description: str, request: Request):
    payments = Payment.list()
    return templates.TemplateResponse("payment.html", {"request": request, "amount": amount, "description": description})


@payment_router.get('/{id}')
async def verify_payment(id: str):
    response = Payment.find_one(id)
    return response

@payment_router.post('/{id}/capture')
async def capture_payment(id: str):
    idempotence_key = str(uuid.uuid4())
    response = Payment.capture(
    id,
    {},
    idempotence_key
    )
    return response

@payment_router.post('/{id}/cancel')
async def cancel_payment(id: str):
    idempotence_key = str(uuid.uuid4())
    response = Payment.cancel(
    id,
    idempotence_key
    )
    return response
