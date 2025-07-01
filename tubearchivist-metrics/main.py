import time

from environment import AppConfig
from getmetrics import GetMetrics
from prometheus_client import Gauge, start_http_server

config = AppConfig().config

# Print configuration on console when starting the application

print("Configuration is currently set to:")
print(f'TA URL: {config["ta_url"]}')
print(f'Listen Port: {config["listen_port"]}')
print(f'Polling interval (seconds): {config["poll_interval"]}')


class AppMetrics:
    # fmt: off
    def __init__(self, poll_interval=int(config["poll_interval"])):

        self.poll_interval = poll_interval

        # Metrics to expose

        self.ignore_downloads = Gauge("yta_ignore_downloads", "Total number of ignored videos")
        self.pending_downloads = Gauge("yta_pending_downloads", "Total number of pending downloads")
        self.pending_videos = Gauge("yta_pending_videos", "Total number of pending video downloads")
        self.pending_shorts = Gauge("yta_pending_shorts", "Total number of pending shorts downloads")
        self.pending_streams = Gauge("yta_pending_streams", "Total number of pending stream downloads")
        # These 3 are sub, sub bits of the tree.
        # I've done all this in a really hacky way that only supports a depth of 1,
        # ideally needs a full rewrite
        # self.watch_total = Gauge("yta_watch_total", "Total number of Videos")
        # self.watch_unwatched = Gauge("yta_watch_unwatched", "Total number of unwatched videos")
        # self.watch_watched = Gauge("yta_watch_watched", "Total number of watched videos")
        self.videos_total = Gauge("yta_videos_total", "Total number of videos")

        self.channel_total = Gauge("yta_channel_total", "Total number of channels")
        self.channel_active = Gauge("yta_channel_active", "Total number of active channels")
        self.channel_inactive = Gauge("yta_channel_inactive", "Total number of inactive channels")
        self.channel_subscribed = Gauge("yta_channel_subscribed", "Total number of subscribed channels")
        self.channel_unsubscribed = Gauge("yta_channel_unsubscribed", "Total number of unsuubscribed channels")

        self.playlists_total = Gauge("yta_playlists_total", "Total number of playlists")
        self.playlists_active = Gauge("yta_playlists_active", "Total number of active playlists")
        self.playlists_inactive = Gauge("yta_playlists_inactive", "Total number of inactive playlists")
        self.playlists_subscribed = Gauge("yta_playlists_subscribed", "Total number of subscribed playlists")
        self.playlists_unsubscribed = Gauge("yta_playlists_unsubscribed", "Total number of unsubscribed playlists")
    # fmt: on

    def run_metrics_loop(self):
        """
        Runs a loop that will update the metrics every poll_interval.
        """
        while True:
            self.retrieve_metrics()
            time.sleep(self.poll_interval)

    def retrieve_metrics(self):
        """
        Retrieves the metrics from the database and updates the metrics.
        """

        print("Obtaining Metrics from API")

        self.pending_downloads.set(GetMetrics.count(index_name="/api/stats/download/", keyvalue="pending"))
        self.ignore_downloads.set(GetMetrics.count(index_name="/api/stats/download/", keyvalue="ignore"))
        self.pending_videos.set(GetMetrics.count(index_name="/api/stats/download/", keyvalue="pending_videos"))
        self.pending_shorts.set(GetMetrics.count(index_name="/api/stats/download/", keyvalue="shorts"))
        self.pending_streams.set(GetMetrics.count(index_name="/api/stats/download/", keyvalue="streams"))
        # Matching 3 for the above commented lines
        # self.watch_total.set(GetMetrics.count(index_name="/api/stats/watch/"))
        # self.watch_unwatched.set(GetMetrics.count(index_name="/api/stats/watch/"))
        # self.watch_watched.set(GetMetrics.count(index_name="/api/stats/watch/"))
        self.videos_total.set(GetMetrics.count(index_name="/api/stats/video/", keyvalue="doc_count"))

        self.channel_total.set(GetMetrics.count(index_name="/api/stats/channel/", keyvalue="doc_count"))
        self.channel_active.set(GetMetrics.count(index_name="/api/stats/channel/", keyvalue="active_true"))
        self.channel_inactive.set(GetMetrics.count(index_name="/api/stats/channel/", keyvalue="active_false"))
        self.channel_subscribed.set(GetMetrics.count(index_name="/api/stats/channel/", keyvalue="subscribed_true"))
        self.channel_unsubscribed.set(GetMetrics.count(index_name="/api/stats/channel/", keyvalue="subscribed_false"))

        self.playlists_total.set(GetMetrics.count(index_name="/api/stats/playlist/", keyvalue="doc_count"))
        self.playlists_active.set(GetMetrics.count(index_name="/api/stats/playlist/", keyvalue="active_true"))
        self.playlists_inactive.set(GetMetrics.count(index_name="/api/stats/playlist/", keyvalue="active_false"))
        self.playlists_subscribed.set(GetMetrics.count(index_name="/api/stats/playlist/", keyvalue="subscribed_true"))
        self.playlists_unsubscribed.set(
            GetMetrics.count(index_name="/api/stats/playlist/", keyvalue="subscribed_false")
        )


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
