FROM python:3.7-alpine

RUN mkdir -p /code
COPY . /code
WORKDIR /code

RUN \
 apk add --no-cache postgresql-libs  libffi-dev && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps

RUN pip install -r requirements.txt

ENV APP_SETTINGS project.server.config.DevelopmentConfig
ENV POSTGRES_SERVER_NAME postgres
ENV POSTGRES_SERVER_PORT 5432
ENV POSTGRES_USER_NAME appscodeuser
ENV POSTGRES_USER_PASS appscodeUser_password

EXPOSE 8000

CMD ["python", "manage.py", "runserver"]
# CMD ["bash", "entrypoint.sh"]
