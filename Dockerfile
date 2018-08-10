FROM ubuntu:latest
MAINTAINER Jinsoo Moon "jinsoo.moon@sk.com"

# Set Locale for cjk
ENV LC_ALL=C.UTF-8

RUN apt-get update -y && apt-get install -y python-pip python-dev build-essential

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app
RUN pip install -r requirements.txt
COPY ./app /app
COPY ./templates /app/templates

ENTRYPOINT ["python"]
CMD ["main.py"]
