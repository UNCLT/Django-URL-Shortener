FROM python:3.9.1
RUN apt-get update -y && apt-get -y upgrade
ENV PYTHONUNBUFFERED 1
RUN mkdir /service
COPY requirements.txt /service/requirements.txt
WORKDIR /service
RUN pip install -r requirements.txt
FROM alpine:edge
RUN apk add --update-cache xclip
ENTRYPOINT xclip

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
