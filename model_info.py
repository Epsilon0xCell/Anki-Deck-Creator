import requests
import json

def get_model_info(model_name):
    # The three calls in this function run in a fixed order, and the
    # order is doing work. I need the name and id map first to know
    # whether the model exists at all. The field and template calls only
    # happen for a model that exists, so a missing model costs exactly
    # one request and returns None below.
    request_payload = {
        "action": "modelNamesAndIds",
        "version": 6
    }
    response = requests.post('http://localhost:8765', json=request_payload)
    result = response.json()
    models = result.get('result', {})
    model_id = models.get(model_name)

    if model_id:
        # The next two calls take the model name, not the id I just
        # looked up. The id is only reported at the end, never used to
        # fetch anything. That reads like a bug on a first pass. It is
        # how these AnkiConnect actions take their input.
        request_payload = {
            "action": "modelFieldNames",
            "version": 6,
            "params": {
                "modelName": model_name
            }
        }
        response = requests.post('http://localhost:8765', json=request_payload)
        fields = response.json().get('result', [])

        request_payload = {
            "action": "modelTemplates",
            "version": 6,
            "params": {
                "modelName": model_name
            }
        }
        response = requests.post('http://localhost:8765', json=request_payload)
        templates = response.json().get('result', {})

        return {
            "model_id": model_id,
            "fields": fields,
            "templates": templates
        }
    else:
        return None

# Edit this value to ask about a different model. Like model_id.py,
# this script takes no command line argument for it.
model_name = "Basic"
try:
    model_info = get_model_info(model_name)
except requests.exceptions.RequestException:
    print("Could not reach AnkiConnect at http://localhost:8765. Is Anki running with the AnkiConnect add-on installed?")
    # This helper exits 1 when Anki is unreachable. model_id.py and
    # all_notes.py print the same message and exit 0. A wrapper reading
    # exit codes would call this run failed and the other two fine for
    # the same problem. The difference is in the files as I wrote them.
    raise SystemExit(1)

if model_info:
    print(f"Model ID for '{model_name}': {model_info['model_id']}")
    print(f"Fields: {model_info['fields']}")
    print(f"Templates: {json.dumps(model_info['templates'], indent=2)}")
else:
    print(f"Model '{model_name}' not found.")
