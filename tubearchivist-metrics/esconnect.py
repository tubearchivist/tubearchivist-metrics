from multiprocessing import AuthenticationError
from elasticsearch import (
    Elasticsearch,
    ConnectionError,
    ConnectionTimeout,
    AuthenticationException,
    AuthorizationException,
)

from environment import AppConfig
from time import sleep


class ElasticWrapper:
    def handle_err(error):
        print("Connection Error: " + str(error))
        print("There was a problem connecting to Elasticsearch")
        print(
            "Please see the error above. This may be as Elasticsearch is still starting up or a misconfiguration"
        )
        print("Sleeping for 10 seconds...")
        sleep(10)

    def get_count(index_name):
        """
        Returns the number of documents in the index
        """
        config = AppConfig().config
        es_url = config["es_url"]
        es_user = config["es_user"]
        es_pass = config["es_pass"]

        es = Elasticsearch(
            [es_url],
            basic_auth=(es_user, es_pass),
            timeout=10,
            max_retries=12,
            retry_on_timeout=True,
        )

        response = 0
        try:
            response = es.count(index=index_name)["count"]
        except AuthenticationException as e:
            ElasticWrapper.handle_err(e)
        except ConnectionError as e:
            ElasticWrapper.handle_err(e)
        except ConnectionTimeout as e:
            ElasticWrapper.handle_err(e)
        except AuthenticationError as e:
            ElasticWrapper.handle_err(e)
        except AuthorizationException as e:
            ElasticWrapper.handle_err(e)
        except:
            print("Unknown error occurred. Check your credentials, url and try again.")
            print("Sleeping for 10 seconds...")
            sleep(10)
        else:
            es.close()
            return response
