# Flask Docker App (CENG413 HW-1) (Based on the CENG413 Week 4 lab app)

```bash
docker build -t hw1-app:1.0 .
docker run -d --name hw1 -p 8000:8000 hw1-app:1.0
curl.exe http://localhost:8000/health
curl.exe http://localhost:8000/version
```