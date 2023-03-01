import random
import requests

def get_random_verse():
    # Read the list of books from the books.txt file
    with open('data/books.txt') as f:
        books = f.readlines()

    # Randomly select a book
    book = random.choice(books).strip()

    # Randomly select a chapter between 1 and 50 (assuming most books have less than 50 chapters)
    chapter = random.randint(1, 50)

    # Randomly select a verse between 1 and 30 (assuming most chapters have less than 30 verses)
    verse = random.randint(1, 30)

    # Construct the URL for the Bible API request
    url = f"https://bible-api.com/{book}+{chapter}:{verse}"

    # Send the request to the Bible API
    response = requests.get(url)
    #print(response.json())

    # Extract the verse text from the response JSON
    verse_text = response.json()['text']

    return verse_text

#print random verse
print(get_random_verse())