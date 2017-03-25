FROM python:3.5

ENV PYTHONUNBUFFERED 1

WORKDIR /app/

RUN adduser --disabled-password --gecos '' myuser 

COPY ./compose/celery/run_celery.sh /run_celery.sh

RUN sed -i 's/\r//' /run_celery.sh \
    && chmod +x /run_celery.sh


ENTRYPOINT ["/run_celery.sh"]
