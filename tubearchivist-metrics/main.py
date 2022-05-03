import time
from prometheus_client import start_http_server, Gauge

from environment import AppConfig
from getmetrics import GetMetrics

config = AppConfig().config

# Print configuration on console when starting the application

print("Configuration is currently set to:")
print(f'Elasticsearch URL: {config["es_url"]}')
print(f'Listen Port: {config["listen_port"]}')
print(f'Polling interval (seconds): {config["poll_interval"]}')


class AppMetrics:
    # fmt: off
    def __init__(self, poll_interval=int(config["poll_interval"])):

        self.poll_interval = poll_interval

        # Metrics to expose
        self.channel_count = Gauge("yta_channel_count", "Number of channels")
        self.playlist_count = Gauge("yta_playlist_count", "Number of playlists")
        self.download_count = Gauge("yta_download_count", "Number of downloads")
        self.download_queue = Gauge("yta_download_queue", "Number of pending downloads")
        self.subtitle_count = Gauge("yta_subtitle_count", "Number of subtitles downloaded for videos")
    # fmt: on

    def run_metrics_loop(self):
        """
        Runs a loop that will update the metrics every second.
        """
        while True:
            self.retrieve_metrics()
            time.sleep(self.poll_interval)

    def retrieve_metrics(self):
        """
        Retrieves the metrics from the database and updates the metrics.
        """
        print("Obtaining Metrics from Elasticsearch")
        self.channel_count.set(GetMetrics.count(index_name="ta_channel"))
        self.playlist_count.set(GetMetrics.count(index_name="ta_playlist"))
        self.download_queue.set(GetMetrics.count(index_name="ta_download"))
        self.download_count.set(GetMetrics.count(index_name="ta_video"))
        self.subtitle_count.set(GetMetrics.count(index_name="ta_subtitle"))


def main():
    """Main Entry Point"""
    listen_port = int(config["listen_port"])
    poll_interval = int(config["poll_interval"])

    app_metrics = AppMetrics(
        poll_interval=poll_interval,
    )
    start_http_server(listen_port)
    app_metrics.run_metrics_loop()


if __name__ == "__main__":
    main()
