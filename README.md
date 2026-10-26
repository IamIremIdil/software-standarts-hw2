# HW-2: Flask app + Redis with Docker Compose

```
docker compose up -d --build   # start app + redis
curl localhost:8000/visit      # counter goes up on each call
docker compose ps              # redis should show "healthy"
docker compose down            # stop, data kept
docker compose down -v         # stop and delete data
```