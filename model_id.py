import requests
import json

def get_model_id(model_name):
    request_payload = {
        "action": "modelNamesAndIds",
        "version": 6
    }
    response = requests.post('http://localhost:8765', json=request_payload)
    result = response.json()
    models = result.get('result', {})
    return models.get(model_name)

model_name = "Basic"  # Replace with the name of your model
try:
    model_id = get_model_id(model_name)
except requests.exceptions.RequestException:
    print("Could not reach AnkiConnect at http://localhost:8765. Is Anki running with the AnkiConnect add-on installed?")
else:
    print(f"Model ID for '{model_name}': {model_id}")
