import json
import requests

# Load the input JSON file
with open('/Users/pranavajk/Translation-Python-Libretranslate/en.json', 'r', encoding='utf-8') as f:
    input_data = json.load(f)

# Define the API endpoint
api_endpoint = 'http://translate.pranavajk.live:5000/translate'

official_en = '/Users/pranavajk/Code/Promethium/pm61datafrontend/public/translations/en.json'
official_ja = '/Users/pranavajk/Code/Promethium/pm61datafrontend/public/translations/ja.json'
official_ko = '/Users/pranavajk/Code/Promethium/pm61datafrontend/public/translations/ko.json'

with open(official_en, 'r', encoding='utf-8') as f:
    official_en_data = json.load(f)
with open(official_ja, 'r', encoding='utf-8') as f:
    official_ja_data = json.load(f)
with open(official_ko, 'r', encoding='utf-8') as f:
    official_ko_data = json.load(f)
# Define a dictionary to store the results
output_data = {}

def translate(text):
    # Send a request to the API with the value
    response = requests.post(api_endpoint, json={'q': text,
        'source': "en",
        'target': "ja",
        'format': "text"})
    
    # Get the result from the API response
    result = response.json()['translatedText']
    
    # Add the result to the output data dictionary
    return result

# Loop through the keys in the input data
for key in input_data.keys():
    # Get the value for the current key
    # if key in official_ko_data.keys():
    #     continue
    value = input_data[key]
    if type(value) is not str:
        sub_data = {}
        for sub_key in value.keys():
            sub_value = value[sub_key]
            # Send a request to the API with the value

            result = translate(sub_value)
            # Add the result to the output data dictionary
            sub_data[sub_key] = result
        output_data[key] = sub_data
    else:
        result = translate(value)
        output_data[key] = result

# Dump the output data to a JSON file
with open('/Users/pranavajk/Translation-Python-Libretranslate/ja.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False)
