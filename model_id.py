import requests
import json

def get_model_id(model_name):
    # I ask for every model name and id in one call and pick mine out of
    # the map here. The whole map crosses the wire to answer one lookup,
    # because this is the AnkiConnect action I have for it.
    request_payload = {
        "action": "modelNamesAndIds",
        "version": 6
    }
    response = requests.post('http://localhost:8765', json=request_payload)
    result = response.json()
    models = result.get('result', {})
    # A name that is not in the map returns None from this get. Nothing
    # here treats None as an error, so the print below says "None" for a
    # missing model. model_info.py handles the same case with a "not
    # found" line instead. The two helpers disagree on this, as written.
    return models.get(model_name)

# This is the value to edit to ask about a different model. There is no
# command line argument for it in any of the helper scripts.
model_name = "Basic"
try:
    model_id = get_model_id(model_name)
except requests.exceptions.RequestException:
    # Wave 1 added this guard. Before it, running this with Anki closed
    # ended in a raw ConnectionError traceback. The message is the same
    # one the other helpers print, and this script then exits 0, where
    # model_info.py exits 1 for the same problem.
    print("Could not reach AnkiConnect at http://localhost:8765. Is Anki running with the AnkiConnect add-on installed?")
else:
    print(f"Model ID for '{model_name}': {model_id}")
