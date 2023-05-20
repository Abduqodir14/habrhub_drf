FROM python:3.10

RUN mkdir /hubrhub

WORKDIR /hubrhub

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

WORKDIR /backend