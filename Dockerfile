FROM theasp/novnc:latest

RUN apt-get update -qq && apt-get update && apt-get install -y python3-pyqt5 python3-pip

WORKDIR /pyqtstopwatch

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY . .
