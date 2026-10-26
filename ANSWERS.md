### 1. How the app finds redis by name

Compose creates one network for the project (`software-standarts-hw2_default`) and attaches both containers to it. Docker runs an embedded DNS server on that network that maps each service name to the container's current IP, so my app, configured with `REDIS_HOST=redis`, reaches Redis. I confirmed it with `gethostbyname('redis')` inside the app container, which printed `172.19.0.2`. The default bridge network used by plain `docker run` has no such DNS, so containers can only reach each other by IP, and those change on every start. My test `docker run --rm alpine ping -c1 a1` failed with `bad address 'a1'` (see the extra screenshot 6).

### 2. Stateless vs. stateful services

The `app` is stateless: it keeps no data on its own disk, and every request reads and writes the counter in Redis. The `redis` service is stateful: it keeps the counter in the `redis-data` named volume. I called `/visit` three times (1, 2, 3), ran `docker compose rm -sf app` and `docker compose down`, started again with `docker compose up -d`, and the next `/visit` returned 4. After `docker compose down -v`, which also deletes the volume, it returned 1, so the data lives in the volume and not in any container.

### 3. Where database passwords should come from

A password should come from the environment at runtime, for example a `.env` file ignored by Git and referenced as `${DB_PASSWORD}` (with a fake `.env.example` committed), or a secrets manager in a real deployment. Committing it is a problem even in a private repository because Git history is permanent: deleting the file later does not remove it from old commits or existing clones, and once it leaks the only fix is to rotate the password. My setup has no password (Redis runs without authentication and its port is not published to the host), so I have no `.env` or `.env.example`, which the assignment only requires if secrets are used.

### Bonus: three copies of the app

I temporarily removed the fixed `8000:8000` mapping so the copies would not fight for the same host port, and ran `docker compose up -d --scale app=3`. Afterwards I restored the mapping, so my final `compose.yaml` publishes port 8000. Requests sent to the three copies (ports 64937, 64938, 64939) returned 1, 2, 3, 4, 5, so the counter was shared. All copies use the same Redis by name, which is why state belongs outside the app.

### AI assistant note

I used an AI assistant to review my files against the checklist and to understand Docker's DNS, the healthcheck setup, and why the counter survived `docker compose down` but not `down -v`. I ran every command myself, and the outputs quoted above are from my own terminal.