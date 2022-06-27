FROM agrigorev/zoomcamp-model:mlops-3.9.7-slim

RUN pip install --upgrade pip

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["gunicorn" ,"-w", "4", "-k", "uvicorn.workers.UvicornWorker" , "--bind", "0.0.0.0:8000", "main:app"]
