### 1. Order of the instructions

My Dockerfile starts with a pinned base image and sets the working directory. It then copies `requirements.txt` and installs the dependencies before copying the rest of the code. Finally, it creates a non-root user, sets the environment variables, and defines the port and start command.

Docker builds images in layers and reuses cached layers as long as nothing in that layer or the previous layers has changed. Since dependencies don't change as often as the code, installing them first means Docker can reuse the cached `pip install` layer when I only edit the code. When I changed `app.py` and rebuilt the image, the build time dropped from 14.4 seconds to 1.6 seconds, and `pip install` showed `CACHED`. If I copied the entire project before installing the dependencies, even a small code change would force Docker to reinstall all the packages.

### 2. Data inside containers

Data written inside a container is stored in its writable layer, which gets deleted when the container is removed. I tested this with my visit counter: after removing the container and starting a new one, the counter started at 1 again.

To keep the data between containers, I mounted a volume using `-v hw1-data:/data`. After removing and recreating the container, the counter continued from 2 to 3 instead of starting over. This showed me why important data shouldn't be stored only inside a container. Containers are meant to be disposable, so data that needs to persist should be stored separately, such as in a database or external storage. A Docker volume is a simple way to achieve this.

### 3. The `latest` tag

The latest tag is a label commonly used for the most recently published image, but it doesn't guarantee that the image is actually the newest version. If the base image uses `latest`, building the same Dockerfile today and six months from now could produce different results if the base image or dependencies have changed, potentially causing unexpected bugs.

To avoid this, I pinned my base image to `python:3.12.11-slim-bookworm`, which specifies the Python version and Debian release. I also pinned the dependencies in `requirements.txt` using `flask==3.1.3` and `gunicorn==23.0.0`. This makes the build more predictable and helps ensure that the project behaves consistently across different environments.

### AI assistant note

I used an AI assistant to help me plan the homework step by step and understand Dockerfile instructions and error messages. I wrote the final answers in my own words and tested the commands and results myself.