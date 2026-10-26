import os
import redis
from flask import Flask

app = Flask(__name__)

GREETING = os.environ.get("APP_GREETING", "Hello")

r = redis.Redis(
    host=os.environ.get("REDIS_HOST", "redis"),
    port=int(os.environ.get("REDIS_PORT", "6379")),
    decode_responses=True,
)

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/greet")
def greet():
    return {"message": GREETING}

@app.route("/visit")
def visit():
    count = r.incr("visits")
    return {"visits": count}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8000")))
    ## The host="0.0.0.0" part matters. Without it, Flask only accepts
    ## connections from inside its own container, and the browser or curl can’t reach it.