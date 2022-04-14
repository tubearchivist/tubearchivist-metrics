from elasticsearch import Elasticsearch
from environment import AppConfig

config = AppConfig().config


class ElasticWrapper:
    """
    makes calls to elastic search
    returns response count
    """

    es_url = config["es_url"]
    es_user = config["es_user"]
    es_pass = config["es_pass"]

    es = Elasticsearch(
        [es_url],
        basic_auth=(es_user, es_pass),
        timeout=30,
        max_retries=10,
        retry_on_timeout=True,
    )

    def get_count(index_name):
        """
        Returns the number of documents in the index
        """
        response = ElasticWrapper.es.count(index=index_name)
        return response["count"]
