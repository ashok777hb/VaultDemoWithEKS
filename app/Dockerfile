FROM python:3.7-alpine

RUN mkdir /app
WORKDIR /app
ADD . /app/
RUN apt-get update; apt-get install curl;pip install -r ./app/requirements.txt

EXPOSE 5000
CMD ["python", "./app/main.py"]