FROM python:alpine

WORKDIR /account_service

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 6800

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6800"]