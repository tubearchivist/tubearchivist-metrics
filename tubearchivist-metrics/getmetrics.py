from esconnect import ElasticWrapper


class GetMetrics:
    @staticmethod
    def count(index_name):

        """Get count of documents from ES"""
        result = ElasticWrapper.get_count(index_name)
        print(f"Metric for {index_name}: {result}")
        return int(result)
