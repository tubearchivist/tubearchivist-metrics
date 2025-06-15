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

        #es_pass = os.environ.get("ES_PASSWORD")
        #es_user = os.environ.get("ES_USER", default="elastic")
        #es_url = os.environ.get("ES_URL", default="http://archivist-es:9200")
        ta_key = os.environ.get("TA_KEY")
        ta_url = os.environ.get("TA_URL")
        listen_port = os.environ.get("LISTEN_PORT", default="9934")
        poll_interval = os.environ.get("POLL_INTERVAL", default="60")

        application = {
            "ta_key": ta_key,
            "ta_url": ta_url,
            #"es_url": es_url,
            #"es_user": es_user,
            #"es_pass": es_pass,
            "listen_port": listen_port,
            "poll_interval": poll_interval,
        }

        return application
