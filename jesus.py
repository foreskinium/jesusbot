import discord
from discord import app_commands
from discord.ext import commands

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

token = ""

@bot.event
async def on_ready():
    
    print("Bot is ready")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)

    #send "hello, {user}" to the channel
    await message.channel.send(f"hello, {username}")
    
#neonoir command
@bot.tree.command(name="hello")
@app_commands.describe(user="do sth")
async def greet(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.send_message("hello")
    


bot.run(token)
