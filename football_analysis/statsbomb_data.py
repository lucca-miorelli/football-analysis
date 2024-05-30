import requests
import json
import pandas as pd

TEST_URL =  "https://raw.githubusercontent.com/statsbomb/open-data/533862946a73608c134d18b78226b6371ce7173c/data/events/3895052.json"

resp = requests.get(TEST_URL)
data = json.loads(resp.text)
# print(data)

# Save as json file in data folder
# with open('data/3895052.json', 'w') as f:
#     json.dump(data, f)


# Explore the data
print(data.keys())

