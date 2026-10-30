import requests
import json

# The three helpers in this file all speak the same AnkiConnect shape:
# an action name, version 6, and params only when the action takes any.
# One thing I keep in mind reading them: I only ever read the "result"
# key. AnkiConnect puts failures in the reply body too, and this file
# never looks at an "error" key, so a failed call and an empty result
# can come back looking the same here.

def get_all_decks():
    request_payload = {
        "action": "deckNames",
        "version": 6
    }
    response = requests.post('http://localhost:8765', json=request_payload)
    return response.json().get('result', [])

def get_all_note_ids(deck_name):
    request_payload = {
        "action": "findNotes",
        "version": 6,
        "params": {
            # I drop the deck name straight into the search string,
            # unquoted. An Anki deck name with a space in it would be
            # read as a deck word plus a loose search word, and the ids
            # could include notes from outside the deck I asked for.
            # The deck names I use have no spaces, so this has not hit
            # me, but the hole is in this line.
            "query": f"deck:{deck_name}"
        }
    }
    response = requests.post('http://localhost:8765', json=request_payload)
    return response.json().get('result', [])

def get_note_info(note_ids):
    request_payload = {
        "action": "notesInfo",
        "version": 6,
        "params": {
            "notes": note_ids
        }
    }
    response = requests.post('http://localhost:8765', json=request_payload)
    return response.json().get('result', [])

def main():
    try:
        decks = get_all_decks()
    except requests.exceptions.RequestException:
        print("Could not reach AnkiConnect at http://localhost:8765. Is Anki running with the AnkiConnect add-on installed?")
        return
    # Only the first call is guarded. "Anki is not running" is the
    # failure I actually hit, and it fails here, on deckNames. If Anki
    # stops after the deck list comes back, the calls inside the loop
    # below raise and this script ends with a traceback. That gap is
    # real and I know it is here.
    all_notes = []

    for deck in decks:
        note_ids = get_all_note_ids(deck)
        # A deck with no notes is skipped by this check instead of
        # sending an empty notes list to notesInfo.
        if note_ids:
            notes = get_note_info(note_ids)
            all_notes.extend(notes)

    # I gather every note from every deck before I print anything.
    # Nothing streams, and the output carries no deck label of mine:
    # each note prints as Anki returns it, in the order the decks came
    # back. On a big collection this is one long JSON dump.
    for note in all_notes:
        print(json.dumps(note, indent=2))

if __name__ == "__main__":
    main()
