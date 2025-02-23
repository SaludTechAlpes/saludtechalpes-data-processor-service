FROM python:3.9-alpine3.16

WORKDIR /app

RUN apk add --no-cache build-base
RUN apk add --no-cache \
    gcc \
    musl-dev \
    linux-headers \
    libffi-dev \
    openssl-dev \
    make \
    python3-dev

COPY . /app
COPY requirements.txt ./
RUN pip install --upgrade "pip<24.1"
RUN pip install -r requirements.txt

EXPOSE 5000

COPY ./docker/start.sh /start.sh
RUN chmod +x /start.sh
CMD ["make", "run-docker"]