from esconnect import ElasticWrapper


class GetMetrics:
    @staticmethod
    def count(index_name):

        """Get count of documents from ES"""
        result = ElasticWrapper.get_count(index_name)
        print("Metric for " + index_name + ": " + str(result))
        return int(result)
