from http.client import FORBIDDEN
from nis import cat
import os
from pkgutil import extend_path
from queue import Empty
import discord
from discord.ext import commands
import pymongo
import logging

TOKEN = str(os.getenv('NERD_BOT'))
password = str(os.environ.get("password"))

admins = [291477074236014593]
client = pymongo.MongoClient("mongodb+srv://koteman123:"+password+"@cluster0.83jlpjn.mongodb.net/?retryWrites=true&w=majority")
mydb = client["nerd-bot"]
nerds = mydb["nerds"]
extremeBool = False

discord.utils.setup_logging(level=logging.NOTSET, root=False)
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='<', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    nerd = nerds.find_one({"discordID": msg.author.id})
    if nerd != None:
        if len(nerd["emoji"]) != 0:
             for x in nerd["emoji"]:
                try:
                    if type(x) == str:
                        await msg.add_reaction(x)
                    elif type(x) == discord.Emoji:
                        if x.is_usable():
                            await msg.add_reaction(str(x))
                except discord.HTTPException:
                    print("Adding the reaction failed.")
                except discord.Forbidden:
                    print("You do not have the proper permissions to react to the message.")
                except discord.NotFound:
                    print("The emoji you specified was not found.")
                except discord.TypeError:
                    print("The emoji parameter is invalid.")
        else:
            await msg.add_reaction("🤓")
    await bot.process_commands(msg)

@bot.command(name="addNerd", description="Adds a nerd. Use the nerd's ID.")
async def addNerd(ctx, chel: discord.Member, *emoji):
    if ctx.author.id not in admins:
        return
    nerd = nerds.find_one({"discordID": chel.id})
    if nerd != None:
        if nerd.discordID == chel.id:
            await ctx.send("already in db")
            return
    if len(emoji) == 0:
        emoji = ["🤓"]
    newNerd = {
        "discordID": chel.id,
        "name": chel.name,
        "emoji": emoji,
    }
    nerds.insert_one(newNerd)
    await ctx.send("successfully added")
        
@bot.command(name="removeNerd", description="amogus")
async def removeNerd(ctx, chel: discord.Member):
    if ctx.author.id not in admins:
        return
    nerd = nerds.find_one({"discordID": chel.id})
    if nerd == None:
        await ctx.send("not in db")
        return
    nerds.delete_one({"discordID": chel.id})
    await ctx.send("successfully deleted")

@bot.command(name="listNerds", description="lists nerds")
async def listNerds(ctx):
    names=""
    for x in nerds.find():
            names += x["name"] + ", "
    names = names[:len(names) - 2]
    if(len(names) == 0):
        names = "No nerds found."
    await ctx.send(names)

bot.run(TOKEN)