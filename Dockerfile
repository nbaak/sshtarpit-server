FROM python:latest

RUN apt-get update && \
    apt-get upgrade -y && \
    pip3 install --upgrade pip && \
    pip3 install prometheus-client && \
    pip3 install requests && \
    echo "DONE"

ADD src/ /tarpit/

EXPOSE 22222
ENTRYPOINT /tarpit/app.py
