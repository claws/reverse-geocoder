FROM python:3.8-alpine

WORKDIR /app

# Preventing Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE 1
# Preventing Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /app/requirements.txt

# install dependencies
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps build-base gcc musl-dev postgresql-dev && \
 python3 -m pip install pip -U && \
 python3 -m pip install -r requirements.txt --no-cache-dir && \
 apk --purge del .build-deps && \
 rm -f /app/requirements.txt

COPY ./app /app/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "info"]
