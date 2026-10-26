FROM python:3.12.11-slim-bookworm

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN useradd --create-home --uid 10001 appuser
USER appuser

ENV APP_VERSION=1.0.0 \
    PYTHONUNBUFFERED=1 \
    PORT=8000
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:${PORT}/health')"

CMD ["sh", "-c", "gunicorn -b 0.0.0.0:${PORT} app:app"]