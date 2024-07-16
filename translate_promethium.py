import json
import requests
from urllib.parse import quote

# Load the input JSON file
with open('/Users/pranavajk/Translation-Python-Libretranslate/en.json', 'r', encoding='utf-8') as f:
    input_data = json.load(f)

# Define the API endpoint
api_endpoint = 'https://translate.pranavajk.com/translate'

official_en = '/Users/pranavajk/Code/Promethium/Node20/pm61datafrontend/public/translations/en.json'
official_ja = '/Users/pranavajk/Code/Promethium/Node20/pm61datafrontend/public/translations/ja.json'
official_ko = '/Users/pranavajk/Code/Promethium/Node20/pm61datafrontend/public/translations/ko.json'

with open(official_en, 'r', encoding='utf-8') as f:
    official_en_data = json.load(f)
with open(official_ja, 'r', encoding='utf-8') as f:
    official_ja_data = json.load(f)
with open(official_ko, 'r', encoding='utf-8') as f:
    official_ko_data = json.load(f)
# Define a dictionary to store the results
output_data = {}
input_data = official_en_data

source_lang = 'en'
target_lang = 'ko'

def translate_text(text, source_lang, target_lang):
    encoded_text = quote(text)
    url = 'https://translate.googleapis.com/translate_a/single?client=gtx&sl={}&tl={}&dt=t&q={}'.format(
        source_lang, target_lang, encoded_text)
    response = requests.get(url)
    translations = []
    if response.ok:
        data = response.json()
        for item in data[0]:
            if item[0]:
                translation = item[0]
                if target_lang == 'ur':
                    translation = translation.replace(", ", "-")
                else:
                    translation = translation.replace(", ", ".")
                if '.' in text:
                    translation = translation.split('. ')[1] if translation.startswith('. ') else translation
                translations.append(translation)
    return " ".join(translations)

def translate(text):
    # Send a request to the API with the value
    response = requests.post(api_endpoint, json={'q': text,
        'source': "en",
        'target': target_lang,
        'format': "text",
        "api_key": "ddaf68b0-1195-4264-b840-f480eb0597e6"})
    
    # Get the result from the API response
    result = response.json()['translatedText']
    
    # Add the result to the output data dictionary
    return result

# Loop through the keys in the input data
for key in input_data.keys():
    # Get the value for the current key
    value = input_data[key]
    if key in official_ja_data.keys() and type(value) is str and target_lang == 'ja':
        continue
    if key in official_ko_data.keys() and type(value) is str and target_lang == 'ko':
        continue
    if type(value) is not str:
        sub_data = {}
        for sub_key in value.keys():
            if sub_key in official_ko_data[key].keys() and target_lang == 'ko':
                continue
            if sub_key in official_ja_data[key].keys() and target_lang == 'ja':
                continue
            sub_value = value[sub_key]
            # Send a request to the API with the value

            # result = translate(sub_value)
            result = translate_text(sub_value, source_lang, target_lang)
            # Add the result to the output data dictionary
            sub_data[sub_key] = result
        if len(sub_data.keys()) == 0:
            continue
        output_data[key] = sub_data
    else:
        # result = translate(value)
        result = translate_text(value, source_lang, target_lang)
        output_data[key] = result

# Dump the output data to a JSON file
with open(f'/Users/pranavajk/Translation-Python-Libretranslate/{target_lang}.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False)
