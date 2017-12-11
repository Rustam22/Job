import json
import requests
import pandas as pd
from pprint import pprint




key = "AIzaSyBkomYP87NuI4koLJNnFDQ"
cx = "001492091657947265563:ncyyguovqo4"



#---------------Prepare The request---------------------#

url = "https://www.googleapis.com/customsearch/v1"
parameters = {
                "q": "halloween",
                "cx": cx,
                "key": key,
              }



#---------------Make the request---------------------#
page = requests.request("GET", url, params=parameters)



#---------------Process Results---------------------#
results = json.loads(page.text)
pprint(results)
print "\n\n"




#---------------Inspecting Results---------------------#
pprint(results.keys())
print "\n\n"



#---------------Process Results Into a Pandas Data Frame---------------------#
def process_search(results):
    link_list = [item["link"] for item in results["items"]]
    df = pd.DataFrame(link_list, columns=["link"])
    df["title"] = [item["title"] for item in results["items"]]
    df["snippet"] = [item["snippet"] for item in results["items"]]
    return df

df = process_search(results)

print df

