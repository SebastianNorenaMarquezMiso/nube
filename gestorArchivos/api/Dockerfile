FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
RUN pip install awscli
ENV AWS_ACCESS_KEY_ID=ASIA3I2TQPFIWOWZUU65
ENV AWS_SECRET_ACCESS_KEY=yWHmBEz6I5JBsxuHJE+U5scVwl5q2jExujoyStZx
COPY . /usr/src/app