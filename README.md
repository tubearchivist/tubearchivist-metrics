# Tube Archivist Metrics
Provide Tube Archivist metrics in Prometheus/OpenMetrics format

This is an optional service as part of the Tube Archivist stack. 

**This is WIP**
---
&nbsp;

## Metrics reported
```
channel_count = Number of channels
playlist_count = Number of playlists
download_count = Number of downloads
download_queue = Number of pending downloads
subtitle_count = Number of subtitles downloaded for videos

```

## Configuration

---
### Environment variables
```
ES_URL: The URL to your ElasticSearch server. Defaults to http://archivist-es:9200
ES_USER: The username for authentication to ElasticSearch. Defaults to elastic
ES_PASSWORD: The password for authentication to ElasticSearch. No default is set.
LISTEN_PORT: The listen port for the metrics server to run on. Defaults to 9934
POLL_INTERVAL: The interval in seconds for the data to be scraped from ElasticSearch. Defaults to 60
```
---
### Running via Docker Compose (supported)
This metrics service is designed to be ran inside of docker.

To view the main compose file for TubeArchivist, please see the main repository here: [TA Repo](https://github.com/bbilly1/tubearchivist)

To add the metrics service in, place this into your compose file and update the environment variables as required.

```
  archivist-metrics:
    image: bbilly1/tubearchivist-metrics:latest
    container_name: archivist-metrics
    restart: always
    environment:
      - "ES_USER=elastic"
      - "ES_PASSWORD=verysecret"
      - "ES_URL=http://archivist-es:9200"
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

To prevent performance issues and unncessecary load on ElasticSearch. We prefetch the metric information from ES every 60 seconds (default). The metric is then updated on the HTTP endpoint after we have retrieved the data and cached for prometheus to scrape.

This means prometheus can scrape the endpoint every second if it likes, but no database calls to ES will be made until the polling interval is reached.

If you require more granular polling, you can update the `POLLING_INTERVAL` environment variable