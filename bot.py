import os
import discord

TOKEN = os.getenv('NERD_BOT')
password = str(os.environ.get("password"))

nerds = [465770139501985812, 291477074236014593]

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_message(msg):
    if msg.author == client.user:
        return
    if msg.author.id in nerds:
        await msg.add_reaction("🤓")
    

client.run(TOKEN)