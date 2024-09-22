FROM python:latest

COPY requirements.txt /tmp/requirements.txt

RUN apt-get update && \
    apt-get upgrade -y && \
    pip3 install --upgrade pip && \
    pip3 install -r /tmp/requirements.txt && \
    echo "DONE"

ADD src/ /tarpit/
WORKDIR /tarpit

EXPOSE 22222
CMD ["/tarpit/entrypoint.sh"]
