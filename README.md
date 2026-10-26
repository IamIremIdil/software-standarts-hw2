# HW-2: Flask app + Redis with Docker Compose

**Start:** `docker compose up -d --build`
**Test:** `curl localhost:8000/visit` (the counter goes up each time)
**Check:** `docker compose ps` (redis should be "healthy")
**Stop:** `docker compose down` (use `docker compose down -v` to delete data)