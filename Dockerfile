# change main.py to simulation.py to run the simulation mode
# Add COPY simulation.py ./
# Change CMD ["python3", "simulation.py"]

FROM python:3.8-slim-buster

RUN apt-get update

WORKDIR /scooter-program

COPY main.py ./
#COPY simulation.py ./
COPY ./src ./src

COPY requirements.txt ./

RUN pip3 install -r requirements.txt

CMD ["python3", "main.py"]
