import json
import requests

api_endpoint = 'https://translate.pranavajk.com/translate'

def translate(text):
    # Send a request to the API with the value
    response = requests.post(api_endpoint, json={'q': text,
        'source': "en",
        'target': "ko",
        'format': "text",
        "api_key": "ddaf68b0-1195-4264-b840-f480eb0597e6"})
    
    # Get the result from the API response
    result = response.json()['translatedText']
    
    # Add the result to the output data dictionary
    return result

from collections import defaultdict

output_data = defaultdict(lambda: defaultdict(lambda: defaultdict(dict)))

with open('/Users/pranavajk/Translation-Python-Libretranslate/connectionDetails.json', 'r', encoding='utf-8') as f:
    input_data = json.load(f)

for ds in input_data.keys():
    output_data[ds] = {}
    for key in input_data[ds].keys():
        if key == "detailsText" or key == "afterTableDetails":
            details = []
            for detail in input_data[ds][key]:
                details.append(translate(detail))
            output_data[ds][key] = details
        if key == "tableData":
            output_data[ds][key] = {}
            for info in input_data[ds][key]:
                output_data[ds][key][info] = {}
                for k in input_data[ds][key][info].keys():
                    output_data[ds][key][info][k] = translate(input_data[ds][key][info][k])

        if key == "FAQ":
            faqs = []
            for faq in input_data[ds][key]:
                sub_faqs = []
                for k in faq:
                    sub_faqs.append(translate(k))
                faqs.append(sub_faqs)
            output_data[ds][key] = faqs

with open('/Users/pranavajk/Translation-Python-Libretranslate/connectionDetailsKo.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False)