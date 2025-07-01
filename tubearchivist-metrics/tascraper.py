import json
from time import sleep

import requests
from environment import AppConfig

# url = "/api/video/<video-id>/"
# headers = {"Authorization": "Token xxxxxxxxxx"}
# response = requests.get(url, headers=headers)


class APIWrapper:

    def handle_err(self, error):
        # None of the below is used. TODO.
        print("Connection Error: " + str(error))
        print("There was a problem connecting to the TA API")
        print("Please see the error above. This may be TA is still starting up or a misconfiguration")
        print("Sleeping for 60 seconds...")
        sleep(60)

    def get_count(self, index_name, keyvalue):

        config = AppConfig().config
        ta_key = config["ta_key"]
        ta_url = config["ta_url"]

        headers = {"Authorization": "Token " + ta_key}

        response = 0

        try:
            # print(ta_url + index_name)
            # print(keyvalue)
            # print("-------------------------------------------------------")

            getjson = requests.get(ta_url + index_name, headers=headers, timeout=30)

            jsonreturn = json.loads(getjson.content)

            response = jsonreturn[keyvalue]
            if response is None:
                response = 0

        except Exception:
            print("No values from " + ta_url + index_name + keyvalue)
            # this has turned into a general failure statement due to bad error management

        return response
