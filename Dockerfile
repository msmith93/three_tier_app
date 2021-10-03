FROM python:3-alpine

RUN apk add python3-dev build-base linux-headers pcre-dev

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY ./helloworld /app

ENTRYPOINT [ "uwsgi" ]

CMD [ "--ini", "/app/helloworld.ini" ]
