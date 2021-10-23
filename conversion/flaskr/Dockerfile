FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install ffmpeg -y
COPY . /usr/src/app