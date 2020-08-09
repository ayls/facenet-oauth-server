FROM python:3.7

WORKDIR /usr/app/
COPY requirements.txt /usr/app/
COPY ./server /usr/app/
EXPOSE 5001

RUN pip install -r requirements.txt

ARG FLASK_ENV=production
ENV FLASK_ENV=$FLASK_ENV

CMD python server.py