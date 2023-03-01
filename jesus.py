import discord
from discord import app_commands
from discord.ext import commands
import asyncio
import random
import requests


from googletrans import Translator

import openai

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

token = ""
openai.api_key = ""

book_chapters = {
    'Genesis': 50, 'Exodus': 40, 'Leviticus': 27, 'Numbers': 36, 'Deuteronomy': 34,
    'Joshua': 24, 'Judges': 21, 'Ruth': 4, '1 Samuel': 31, '2 Samuel': 24,
    '1 Kings': 22, '2 Kings': 25, '1 Chronicles': 29, '2 Chronicles': 36,
    'Ezra': 10, 'Nehemiah': 13, 'Esther': 10, 'Job': 42, 'Psalms': 150,
    'Proverbs': 31, 'Ecclesiastes': 12, 'Song of Solomon': 8, 'Isaiah': 66,
    'Jeremiah': 52, 'Lamentations': 5, 'Ezekiel': 48, 'Daniel': 12, 'Hosea': 14,
    'Joel': 3, 'Amos': 9, 'Obadiah': 1, 'Jonah': 4, 'Micah': 7, 'Nahum': 3,
    'Habakkuk': 3, 'Zephaniah': 3, 'Haggai': 2, 'Zechariah': 14, 'Malachi': 4,
    'Matthew': 28, 'Mark': 16, 'Luke': 24, 'John': 21, 'Acts': 28,
    'Romans': 16, '1 Corinthians': 16, '2 Corinthians': 13, 'Galatians': 6,
    'Ephesians': 6, 'Philippians': 4, 'Colossians': 4, '1 Thessalonians': 5,
    '2 Thessalonians': 3, '1 Timothy': 6, '2 Timothy': 4, 'Titus': 3,
    'Philemon': 1, 'Hebrews': 13, 'James': 5, '1 Peter': 5, '2 Peter': 3,
    '1 John': 5, '2 John': 1, '3 John': 1, 'Jude': 1, 'Revelation': 22
}

@bot.event
async def on_ready():
    
    print("Bot is ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


@bot.tree.command(name="klausti")
@app_commands.describe(prompt="Užduok klausimą")
async def chat(interaction: discord.Interaction, prompt: str):
    await interaction.response.defer()
    try:
        #debug print prompt
        print(prompt)

        translator = Translator()
        translation = translator.translate(prompt, dest='en')

        #debug print translated to english prompt
        print(translation.text)

        prompt_jesus = '''
        You: Dear Jesus, please answer my question. 
        Jesus Christ: What is your question, my child? 
        You: {}
        Jesus Christ:  
        '''.format(translation.text)

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt_jesus,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        #debug print response text
        print(response['choices'][0]['text'])

        response_text = response['choices'][0]['text']

        response_text_translated = translator.translate(response_text, dest='lt')

        #debug print translated to lithuanian response text
        print(response_text_translated.text)

        final_response = "{user}: {prompt}\n\n**{response}**".format(user=interaction.user.mention, prompt=prompt, response=response_text_translated.text)

        print("####################")

        await interaction.followup.send(final_response)

    except Exception as e:
        print("Error:", e)
        await interaction.followup.send("Klaida! Perdaug simbolių arba dar kažkas neveikia.", ephemeral=True)


@bot.tree.command(name="biblijoseilute")
async def hello(interaction: discord.Interaction):
    await interaction.response.defer() 

    while True:        
        try:
            book = random.choice(list(book_chapters.keys()))
            chapter = random.randint(1, book_chapters[book])
            # Randomly select a verse
            verse = random.randint(1, 50)
            # Print the selected book and chapter
            print(f"{book} {chapter}:{verse}")
            # Construct the API endpoint URL
            endpoint = f"https://bible-api.com/{book}+{chapter}:{verse}"
            # Make a GET request to the endpoint and get the response JSON
            response = requests.get(endpoint).json()
            # Extract the verse text from the response JSON
            verse_text = response['text']
            # Print the verse text
            verse_text_with_name = f"{verse_text}{book} {chapter}:{verse}"

            translator = Translator()
            translation = translator.translate(verse_text_with_name, dest='lt')

            #debug print translated to english prompt
            print(translation.text)
            await interaction.followup.send(translation.text)

            break
        except Exception as e:
            # If there is no verse for the selected chapter and verse, try again
            print("Error:", e)
            continue



    


bot.run(token)
