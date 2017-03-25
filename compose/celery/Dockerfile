FROM python:3.5

ENV PYTHONUNBUFFERED 1

COPY ./compose/celery/run_celery.sh /run_celery.sh

RUN sed -i 's/\r//' /run_celery.sh \
    && chmod +x /run_celery.sh

WORKDIR /app

ENTRYPOINT ["/run_celery.sh"]
