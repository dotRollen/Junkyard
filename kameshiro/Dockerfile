FROM python:3.6.4
MAINTAINER Edward Nunez <edward_nunez@shi.com>

RUN apt-get update -qq \
    && apt-get install -y netcat \
    && rm -rf /var/lib/apt/lists/* 

ADD . /usr/local/kitsu/backend 

WORKDIR /usr/local/kitsu/backend

RUN mkdir -p /usr/local/kitsu \
    && useradd -d /usr/local/kitsu kitsu \
    && mkdir /usr/local/kitsu/logs \
	&& pip install -r requirements.txt \
    && chmod +x ./start 

CMD ["./start"]