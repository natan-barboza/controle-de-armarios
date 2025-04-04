    FROM python:3.13.2-alpine3.21 AS builder

    RUN mkdir /app

    WORKDIR /app

    ENV PYTHONDONTWRITEBYTECODE=1

    ENV PYTHONUNBUFFERED=1 

    RUN pip install --upgrade pip 

    COPY requirements.txt  /app/

    RUN pip install --no-cache-dir -r requirements.txt

    FROM python:3.13.2-alpine3.21

    RUN adduser -D -g '' app-admin && \
    mkdir /app && \
    chown -R app-admin /app

    COPY --from=builder /usr/local/lib/python3.13/site-packages/ /usr/local/lib/python3.13/site-packages/
    COPY --from=builder /usr/local/bin/ /usr/local/bin/

    WORKDIR /app

    COPY --chown=app-admin:app-admin . .

    RUN python manage.py collectstatic --noinput

    ENV PYTHONDONTWRITEBYTECODE=1
    ENV PYTHONUNBUFFERED=1

    USER app-admin

    EXPOSE 8000

    COPY --chown=app-admin:app-admin entrypoint.sh /app/entrypoint.sh
    ENTRYPOINT ["/app/entrypoint.sh"]