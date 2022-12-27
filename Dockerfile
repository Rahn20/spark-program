FROM python:3.8-slim-buster

RUN apt-get update

WORKDIR /scooter-program

COPY main.py ./
COPY ./src ./src

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

# change main.py to simulation.py to run the simulation mode

CMD ["python3", "main.py"]
