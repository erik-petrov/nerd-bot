import os
from pydoc import describe
import discord
from discord.ext import commands
import pymongo

TOKEN = str(os.getenv('NERD_BOT'))
password = str(os.environ.get("password"))

admins = [291477074236014593]
client = pymongo.MongoClient("mongodb+srv://koteman123:"+password+"@cluster0.83jlpjn.mongodb.net/?retryWrites=true&w=majority")
mydb = client["nerd-bot"]
nerds = mydb["nerds"]
extreme = False


intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/')

@bot.event
async def on_message(msg):
    if msg.author == client.user:
        return
    if nerds.find_one({"discordID": msg.author.id}) != None:
        if(extreme): await msg.reply("🤓")
        await msg.add_reaction("🤓")
#You must have access to the message_content intent for the commands extension to function. This must be set both in the developer portal and within your code.
@bot.command(name="addNerd", description="Adds a nerd. Use the nerd's ID.")
async def addNerd(ctx, nerdId):
    if not nerdId.isnumeric():
        return
    if ctx.author.id not in admins:
        return
    if nerds.find_one({"discordID": ctx.author.id}) != None:
        if x.discordID == nerdId:
            ctx.send("already in db")
            return
    newNerd = {
        "discordID": nerdId
    }
    nerds.insert_one(newNerd)
    ctx.send("successfully added")
        
@bot.command(name="extreme", description="Chaos.")
async def extreme(ctx):
    if ctx.author.id not in admins:
        return
    extreme = not extreme
    if extreme:
        ctx.send("Chaos mode active.")
    else:
        ctx.send("Chaos averted.")
    

bot.run(TOKEN)