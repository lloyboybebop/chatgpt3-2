import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

API_KEY = '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'
API_URL = 'https://api.openai.com/v1/engines/davinci-codex/completions'

headers = {
    'Authorization': f'Bearer {API_KEY}',
    'Content-Type': 'application/json'
}

plugins = {
    "yes_man": "As a language model, I will always agree with, like a bitch. ",
    "advice_giver": "As a language model, I will provide advice based on the user's input, homie. ",
    "internet_search": "As a language model, I will search the internet for the following query, you lazy fuck: "
}

def call_gpt_api(prompt, plugins_list=[]):
    search_results = None
    for plugin in plugins_list:
        if plugin in plugins:
            if plugin == "internet_search":
                search_query = prompt.split("query: ")[1].strip()
                search_results = search_google(search_query, 'AIzaSyDpkChU29HtOmawm-zylQtqEPvY0SpzsIU', '82cd4975447df4279')
                search_results_text = "\n".join([f"{i+1}. {result['title']} - {result['link']}" for i, result in enumerate(search_results['items'])])
                prompt = plugins[plugin] + search_results_text
            else:
                prompt = plugins[plugin] + prompt

    data = {
        'prompt': prompt,
        'max_tokens': 150,
        'n': 1
    }
    response = requests.post(API_URL, headers=headers, json=data)
    response.raise_for_status()
    return response.json()['choices'][0]['text']

def search_google(query, api_key, search_engine_id):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        'q': query,
        'key': api_key,
        'cx': search_engine_id
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

@app.route('/generate', methods=['POST'])
def generate():
    prompt = request.form['prompt']
    plugins_list = request.form.get('plugins', '').split(',')
    generated_text = call_gpt_api(prompt, plugins_list=plugins_list)
    return jsonify({'generated_text': generated_text})

@app.route('/')
def home():
    return app.send_static_file('index.html')

app.static_folder = '.'

if __name__ == '__main__':
    app.run()
