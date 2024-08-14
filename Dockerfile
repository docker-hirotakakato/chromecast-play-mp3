FROM alpine:latest

WORKDIR /opt/chromecast-play-mp3

RUN apk add --no-cache py3-flask py3-gunicorn py3-pychromecast

COPY main.py .

CMD ["gunicorn", "-b=:80", "--access-logfile=-", "main:app"]
