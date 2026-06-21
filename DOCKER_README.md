# Docker: Build and Run

This project includes Docker artifacts to run the Animal Detection app in a container.

Prerequisites
- Docker Desktop for Windows (https://www.docker.com/products/docker-desktop)
- Optional: WSL2 back-end for better performance

Quick start (recommended)

1. Install Docker Desktop and start it.
2. Open PowerShell in the project root (where this README and `Dockerfile` are located).
3. (Optional) Set Telegram environment variables in your session if you want alerts:

```powershell
$env:TELEGRAM_BOT_TOKEN = "your_bot_token"
$env:TELEGRAM_CHAT_ID = "your_chat_id"
```

4. Use the helper script to build and run the container:

```powershell
.\run_docker.ps1 -Build -Recreate
```

This will:
- Build the Docker image `animal-detection:local` (if not present)
- Run the container `animal-detection-local` mapping host ports and volumes
- Tail container logs; press Ctrl+C to stop viewing logs (container keeps running)

Manual build & run

Build image:

```powershell
docker build -t animal-detection:local .
```

Run container:

```powershell
docker run -d --name animal-detection-local -p 5000:5000 \
  -v ${PWD}/snapshots:/app/snapshots \
  -v ${PWD}/logs:/app/logs \
  -v ${PWD}/runs:/app/runs \
  -e TELEGRAM_BOT_TOKEN="${env:TELEGRAM_BOT_TOKEN}" \
  -e TELEGRAM_CHAT_ID="${env:TELEGRAM_CHAT_ID}" \
  animal-detection:local

docker logs -f animal-detection-local
```

Access the dashboard
- The Flask dashboard runs on port 5000 inside the container. Open:

```
http://localhost:5000
```

Notes & troubleshooting
- If you need GPU support, configure NVIDIA Container Toolkit and adjust the `docker run` or `docker-compose` configuration to expose GPUs.
- To allow the container to access a local webcam, you will need special device mapping; this is platform-dependent and not recommended for production containers.
- If the container fails to start due to Python package compatibility, prefer running the app locally in a virtualenv (see `setup_env.ps1`).

Stopping and removing

```powershell
docker stop animal-detection-local
docker rm animal-detection-local
docker image rm animal-detection:local
```

If you want me to run the Docker build and run steps here, install Docker Desktop and tell me when it's available — I will run `.\run_docker.ps1 -Build -Recreate` and show the logs. 
