import discord
from discord import app_commands
from discord.ext import commands
import asyncio


from googletrans import Translator

import openai


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

token = ""
openai.api_key = ""

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
        await interaction.followup.send("Kažkas neveikia", ephemeral=True)





    


bot.run(token)
