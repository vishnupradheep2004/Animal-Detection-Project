<#
Helper script to build and run the project's Docker image on Windows.

Usage (PowerShell, run as admin if needed):
  .\run_docker.ps1 [-Build] [-Recreate] [-Remove] [-Compose]

Options:
  -Build     : Build the Docker image (default if image not found)
  -Recreate  : Stop and remove any existing container, then run a new one
  -Remove    : Remove the container and image
  -Compose   : Use docker-compose up --build instead of docker run

Notes:
- Requires Docker Desktop (Windows) to be installed and running.
- Maps local `snapshots`, `logs`, and `runs` into the container.
- Exposes the app on port 5000.
#>

param(
    [switch]$Build,
    [switch]$Recreate,
    [switch]$Remove,
    [switch]$Compose
)

function Test-Docker {
    try {
        docker --version | Out-Null
        return $true
    } catch {
        return $false
    }
}

if (-not (Test-Docker)) {
    Write-Error "Docker CLI not found. Install Docker Desktop and ensure `docker` is on PATH."
    exit 1
}

$imageName = "animal-detection:local"
$containerName = "animal-detection-local"

if ($Remove) {
    Write-Host "Removing container and image..."
    docker rm -f $containerName -v 2>$null | Out-Null
    docker image rm $imageName -f 2>$null | Out-Null
    Write-Host "Removed (if present)."
    exit 0
}

if ($Compose) {
    Write-Host "Running with docker-compose..."
    docker-compose up --build
    exit $LASTEXITCODE
}

# Build if requested or image not present
$imageExists = (docker images -q $imageName) -ne ""
if ($Build -or -not $imageExists) {
    Write-Host "Building Docker image: $imageName"
    docker build -t $imageName .
    if ($LASTEXITCODE -ne 0) { Write-Error "Docker build failed"; exit $LASTEXITCODE }
}

if ($Recreate) {
    Write-Host "Stopping existing container (if any)..."
    docker rm -f $containerName -v 2>$null | Out-Null
}

# Run container with recommended volume mounts and port mapping
Write-Host "Starting container: $containerName"
docker run -d --name $containerName `
    -p 5000:5000 `
    -v ${PWD}\snapshots:/app/snapshots `
    -v ${PWD}\logs:/app/logs `
    -v ${PWD}\runs:/app/runs `
    -e TELEGRAM_BOT_TOKEN="$env:TELEGRAM_BOT_TOKEN" `
    -e TELEGRAM_CHAT_ID="$env:TELEGRAM_CHAT_ID" `
    $imageName

if ($LASTEXITCODE -ne 0) { Write-Error "docker run failed"; exit $LASTEXITCODE }

Write-Host "Container started. To follow logs run: docker logs -f $containerName"
docker logs -f $containerName
