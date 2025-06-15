from tascraper import APIWrapper


class GetMetrics:
    @staticmethod
    def count(index_name, keyvalue):

        """Get count of documents from API"""
        result = APIWrapper.get_count(index_name, keyvalue)
        #print(f"Metric for {index_name}: {keyvalue}: {result}")
        return result
