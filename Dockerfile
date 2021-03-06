FROM python:3.9.5-alpine

ARG GECKODRIVER_URL=https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz

COPY ./main.py /usr/bin/slack-batch
COPY ./requirements.txt /tmp/requirements.txt

# Install GeckoDriver
RUN apk update && apk upgrade \
    && wget $GECKODRIVER_URL -O /tmp/geckodriver.tar.gz \
    && tar -zxf /tmp/geckodriver.tar.gz -C /usr/bin \
    && apk add firefox-esr \
    && pip install -r /tmp/requirements.txt \
    && mkdir /var/screenshots \
    && chmod u+x /usr/bin/slack-batch

WORKDIR /tmp/files

ENTRYPOINT ["/usr/bin/slack-batch"]