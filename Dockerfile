FROM python:3.8-slim-buster

RUN apt-get update

WORKDIR /scooter-program

COPY main.py ./
COPY ./src ./src

CMD ["python3", "main.py"]