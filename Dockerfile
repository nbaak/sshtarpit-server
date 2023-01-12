FROM python:latest

RUN apt-get update && \
    apt-get upgrade -y && \
    pip3 install --upgrade pip && \
    echo "DONE"

ADD src/ /tarpit/

EXPOSE 22222
ENTRYPOINT /tarpit/App.py
