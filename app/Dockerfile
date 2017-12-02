FROM ubuntu:latest
  
MAINTAINER Yujia Liu "sophialyj07@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./ /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENTRYPOINT [ "python3" ]

CMD [ "./web_app/app.py" ]
