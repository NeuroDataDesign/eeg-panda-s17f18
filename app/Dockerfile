FROM ubuntu:latest
  
MAINTAINER Yujia Liu "sophialyj07@gmail.com"

ADD credentials /credentials
RUN mkdir /.aws
RUN mv credentials /.aws/credentials
RUN mv /.aws ${HOME}/.aws
RUN cat ${HOME}/.aws/credentials

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev python3-tk


COPY ./ /app

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install awscli


ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
