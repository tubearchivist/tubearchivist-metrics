"""
Functionality for setting up the environment for the metrics package.
Reads in environment variables for the application to use.
"""

import os


class AppConfig:
    def __init__(self) -> None:
        self.config = self.get_config()

    @staticmethod
    def get_config():
        """
        Reads in environment variables for the application to use.
        """

        ta_key = os.environ.get("TA_KEY")
        ta_url = os.environ.get("TA_URL")
        listen_port = os.environ.get("LISTEN_PORT", default="9934")
        poll_interval = os.environ.get("POLL_INTERVAL", default="120")

        application = {
            "ta_key": ta_key,
            "ta_url": ta_url,
            "listen_port": listen_port,
            "poll_interval": poll_interval,
        }

        return application
