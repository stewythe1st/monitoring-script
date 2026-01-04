# Monitoring Script

Simple script to monitor and notify when server(s) go down.

## Deploy

```bash
docker buildx build --platform linux/arm64/v8 --load -t stewythe1st/monitoring-script .
docker tag stewythe1st/monitoring-script:latest stewythe1st/monitoring-script:v0.0.x
docker push stewythe1st/monitoring-script:v0.0.x
```