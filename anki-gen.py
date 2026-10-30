import genanki
import random
import string

def random_string(length=10):
    # ascii_letters only, no digits and no symbols. A name built here
    # drops into a file name on any system without quoting trouble.
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def read_flashcards(file_path):
    with open(file_path, 'r') as file:
        # I drop blank lines before I parse anything. flashcards.txt
        # uses blank lines to separate cards for a human reader, so a
        # raw parse would land a blank line where an answer or a
        # category should be.
        # The trade is that positions after this point count cleaned
        # lines, not lines in the file. The warnings below number the
        # cleaned list, so they will not match what an editor shows.
        lines = [line.strip() for line in file if line.strip()]

    flashcards = []
    i = 0
    while i < len(lines):
        # This parser rests on one rule of the input format: a question
        # is a line that ends with "?". A category line ending in "?"
        # would be read as the next question, and an answer ending in
        # "?" would end its own card early. The format has no other
        # marker, so that question mark is the whole signal.
        if not lines[i].endswith('?'):
            print(f"Warning: Incomplete flashcard entry starting at line {i+1}")
            break
        question = lines[i]
        i += 1
        if i >= len(lines):
            print(f"Warning: Missing answer for question starting at line {i}")
            break
        answer = lines[i]
        i += 1
        categories = []
        # The category lines follow their own card's answer in the
        # file, so I collect them here, after the answer, until the
        # next question line. I once collected them before the question
        # instead, and Wave 1 found the result inside the generated
        # deck: the first card had no categories, every other card
        # carried the card before it, and the file ended with a warning
        # about an entry that was really just trailing categories.
        # Both warnings above stop the parse with break. One bad entry
        # costs every card after it, not just its own. I would rather
        # lose the tail of a malformed file than guess where the next
        # card starts.
        while i < len(lines) and not lines[i].endswith('?'):
            categories.append(lines[i])
            i += 1
        flashcards.append((question, answer, categories))
    return flashcards

# The model id is a fixed number I picked once. genanki wants an id
# that stays stable for a model: if this changed between runs, Anki
# would treat the same three fields as a new note type on import.
model = genanki.Model(
  1607392319,
  'AnkiGen',
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
    {'name': 'Categories'},
  ],
  templates=[
    {
      'name': 'Card 1',
      # I put Categories on the question side, in italics under the
      # question, so a card shows its topic before it is flipped. The
      # answer side repeats the whole front through FrontSide and then
      # adds the answer under the rule.
      'qfmt': '{{Question}}<br><br><i>{{Categories}}</i>',
      'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
    },
  ])

# Everything from here down runs at import time. There is no main guard
# in this file, so importing anki-gen to borrow read_flashcards would
# build a deck and write a file as a side effect. I run this file as a
# script. I do not import it.

# I name the deck and the file with random strings instead of asking
# anyone to pick a name. Each run writes under a fresh name instead of
# overwriting the last deck. The cost is gibberish deck names inside
# Anki after import, which I accept.
deck_name = random_string()
file_name = f'{random_string()}.apkg'

deck = genanki.Deck(
  random.randint(1 << 30, 1 << 31),
  deck_name)

# The input path is fixed relative to where I run the script. Run it
# from another folder and it looks for flashcards.txt there, not next
# to this file.
flashcards = read_flashcards('flashcards.txt')

for question, answer, categories in flashcards:
  note = genanki.Note(
    model=model,
    # The category list becomes one field, joined with ", ". After this
    # join the list is gone, so a category that contained a comma of its
    # own could not be told apart from two categories in the deck.
    fields=[question, answer, ', '.join(categories)])
  deck.add_note(note)

package = genanki.Package(deck)
package.write_to_file(file_name)

print(f'Deck "{deck_name}" has been created and saved as "{file_name}".')
