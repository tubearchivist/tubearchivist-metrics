# Tube Archivist Metrics
Provide Tube Archivist metrics in Prometheus/OpenMetrics format

This is an optional service as part of the Tube Archivist stack. 

**This is WIP**
---
&nbsp;

## Metrics reported
```
yta_ignore_downloads, Total number of ignored videos
yta_pending_downloads, Total number of pending downloads
yta_pending_videos, Total number of pending video downloads
yta_pending_shorts, Total number of pending shorts downloads
yta_pending_streams, Total number of pending stream downloads

yta_videos_total, Total number of videos
        
yta_channel_total, Total number of channels
yta_channel_active, Total number of active channels
yta_channel_inactive, Total number of inactive channels
yta_channel_subscribed, Total number of subscribed channels
yta_channel_unsubscribed, Total number of unsuubscribed channels
        
        
        
yta_playlists_total, Total number of playlists
yta_playlists_active, Total number of active playlists
yta_playlists_inactive, "Total number of inactive playlists
yta_playlists_subscribed, Total number of subscribed playlists
yta_playlists_unsubscribed, Total number of unsubscribed playlists

```

## Configuration

---
### Environment variables
```
TA_URL: The URL to your TubeArchivist Server
TA_KEY: Your TubeArchivist API key
LISTEN_PORT: The listen port for the metrics server to run on. Defaults to 9934
POLL_INTERVAL: The interval in seconds for the data to be scraped from ElasticSearch. Defaults to 60
```
---
### Running via Docker Compose (supported)
This metrics service is designed to be ran inside of docker.

To view the main compose file for TubeArchivist, please see the main repository here: [TA Repo](https://github.com/tubearchivist/tubearchivist)

To add the metrics service in, place this into your compose file and update the environment variables as required.

```
  archivist-metrics:
    image: bbilly1/tubearchivist-metrics:latest
    container_name: archivist-metrics
    restart: always
    environment:
      - "TA_URL=http://tubearchivist.local"
      - "TA_KEY="your ta api key"
      - "LISTEN_PORT=9934"
      - "POLL_INTERVAL=60"
    ports:
      - 9934:9934
```
---

### Running via Standalone
Should you want to, you can install and run this without docker.

To do so, clone this repo, install the python libraries with `pip3 install -r requirements.txt`

then run `python3 tubearchivist-metrics/main.py`

Environment variables can be passed in via normal syntax for your OS.

---

### Prometheus example config
```
      - job_name: 'tubearchivist-metrics'
        metrics_path: /
        static_configs:
          - targets:
              - <server>:9934
```
---
## How are metrics gathered?

Typically, a prometheus server will poll the HTTP endpoint of the metrics service to obtain its metrics.

In most scenarios, a service will then retrieve the data for the metric, and then respond to the prometheus http call. However this can be quite harsh on databases and applications, especially when prometheus is polling every 15 seconds.

To prevent performance issues and unncessecary load on ElasticSearch. We prefetch the metric information from the API every 60 seconds (default). The metric is then updated on the HTTP endpoint after we have retrieved the data and cached for prometheus to scrape.

This means prometheus can scrape the endpoint every second if it likes, but no database calls to the API will be made until the polling interval is reached.

If you require more granular polling, you can update the `POLLING_INTERVAL` environment variable