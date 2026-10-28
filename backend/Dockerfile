
FROM python:3.13.16-slim-trixie

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir --upgrade pip setuptools wheel \
    && python -m pip install --no-cache-dir -r requirements.txt

COPY app.py .

ENV REGNO=202401100500199
ARG APP_VERSION=0.2
ENV APP_VERSION=${APP_VERSION}

RUN useradd --create-home --uid 10001 appuser \
    && chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
