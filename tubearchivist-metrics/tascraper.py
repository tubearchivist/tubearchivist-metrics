import requests
import json

#url = "/api/video/<video-id>/"
#headers = {"Authorization": "Token xxxxxxxxxx"}
#response = requests.get(url, headers=headers)

from environment import AppConfig
from time import sleep


class APIWrapper:
    def handle_err(error):
        print("Connection Error: " + str(error))
        print("There was a problem connecting to the TA API")
        print(
            "Please see the error above. This may be TA is still starting up or a misconfiguration"
        )
        print("Sleeping for 60 seconds...")
        sleep(60)

    def get_count(index_name, keyvalue):
        """
        Returns the number of documents in the index
        """
        config = AppConfig().config
        ta_key = config["ta_key"]
        ta_url = config["ta_url"]

        headers = {"Authorization": "Token " + ta_key}
        #print(headers)
        response = 0

        try:
            #print(ta_url + index_name)
            #print(keyvalue)
            #print("-------------------------------------------------------")
        
            beans = requests.get(ta_url + index_name, headers=headers)
            #print(beans.json())
            jsonreturn = json.loads(beans.content)
            #print (jsonreturn)
        
            response = jsonreturn[keyvalue]
            if response is None:
                response = 0
   #     print(jsonreturn)
        #response = 0
            
        except:
            print("No values from " + ta_url + index_name + keyvalue)

        return response
        
