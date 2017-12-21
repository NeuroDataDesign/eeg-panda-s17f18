FROM ubuntu:latest
  
MAINTAINER Yujia Liu "sophialyj07@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python3-pip python3-dev python3-tk

ADD credentials.csv /credentials.csv
# We copy just the requirements.txt first to leverage Docker cache
RUN mkdir /.aws && printf "[default]\nregion = us-east-1" > /.aws/config
RUN printf "[default]\n`tail -n 1 /credentials.csv | cut -d',' -f2`\n`tail -n 1 /credentials.csv | cut -d',' -f3`" > /.aws/credentials && mv /.aws/  ${HOME} && rm /credentials.csv
RUN cat ${HOME}/.aws/credentials


COPY ./ /app

WORKDIR /app

RUN pip3 install -r requirements.txt
RUN pip3 install awscli


ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
