![banner](assets/banner.png)

# Anki-Deck-Creator

Creates Anki decks (.apkg files) from a plain text file of flashcards, plus three small helper scripts that query a running Anki instance through the AnkiConnect add-on.

## Files

- `anki-gen.py` - builds an .apkg deck from `flashcards.txt` using genanki. The deck name and the output file name are random strings, so each run produces a new file such as `jTHjjbWTMJ.apkg`.
- `flashcards.txt` - the sample input: 55 cards about the branches of the United States government.
- `all_notes.py` - prints every note in every deck as JSON, using AnkiConnect.
- `model_id.py` - prints the numeric ID of the model named `Basic`, using AnkiConnect.
- `model_info.py` - prints the ID, field names, and templates of the model named `Basic`, using AnkiConnect.
- `.github/workflows/anki-decks-gen.yml` - on every push to `main`, installs genanki, runs `anki-gen.py`, uploads the .apkg as a workflow artifact, and creates a GitHub release with the .apkg attached.

## Input format

`read_flashcards` in `anki-gen.py` strips blank lines, then reads each card as:

1. A question line, ending with `?`
2. One answer line
3. Zero or more category lines, which belong to that card and run until the next question line

The generated model has three fields: Question, Answer, and Categories (the category lines joined with commas).

## Requirements

- Python 3
- For `anki-gen.py`: `genanki`
- For the helper scripts: `requests`, plus Anki running with the AnkiConnect add-on listening at `http://localhost:8765`

Install both Python packages with:

```
pip install -r requirements.txt
```

## Usage

Generate a deck:

```
python anki-gen.py
```

The script prints the random deck name and the .apkg file name it created. Import that .apkg file into Anki to use the deck.

Run a helper script (Anki must already be running):

```
python all_notes.py
python model_id.py
python model_info.py
```

If AnkiConnect cannot be reached, the helper scripts now print a short message saying so instead of a traceback. To query a model other than `Basic`, edit the `model_name` value in `model_id.py` or `model_info.py`.
