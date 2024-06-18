FROM python:3.10

RUN mkdir /kimchistopback

WORKDIR /kimchistopback

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn app:app --workers 3 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000