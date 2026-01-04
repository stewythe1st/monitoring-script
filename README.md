# Monitoring Script

Simple script to monitor and notify when server(s) go down.

## Deploy

```bash
docker build -t stewythe1st/monitoring-script .
docker tag stewythe1st/monitoring-script:latest stewythe1st/monitoring-script:v0.0.x
docker push stewythe1st/monitoring-script:v0.0.x
```