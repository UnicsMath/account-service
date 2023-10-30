FROM python:alpine

WORKDIR /account_service

COPY requirements.txt .

RUN apk update && \
    apk add --no-cache freetds-dev build-base openssl-dev libffi-dev krb5-dev && \
    pip install --upgrade pip && \
    pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE 6800

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6800"]