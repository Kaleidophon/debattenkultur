FROM python:3.6
MAINTAINER Kaleidophon (https://github.com/Kaleidophon)

RUN mkdir -p /parser/
WORKDIR /parser/

COPY ./ ./

ENV PYTHONPATH=/parser/

RUN pip3 install -r ./requirements.txt

RUN ls -lah

CMD python3 ./parser.py
