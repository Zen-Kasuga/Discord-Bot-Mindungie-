import discord
from discord.ext import commands
import os
import random
from dotenv import load_dotenv
import pandas as pd
from tabulate import tabulate
from sklearn.linear_model import LinearRegression

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default() #This shi filters what messages the bot WANT to receive

intents.message_content = True #Encryption thingy, it allows the bot to view discord messages

bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def Analyze(ctx, y):
    print(ctx.author)
    print(ctx.channel)
    print(ctx.guild)

    x_variable = []

    if not ctx.message.attachments:
        await ctx.send(f"This is no attachment, {ctx.author}. You dumb fuck!!")
        return 

    for attachment in ctx.message.attachments:
        if attachment.filename.endswith(".csv"):
            await attachment.save(attachment.filename)
            file_path = attachment.filename
            dataFrame = pd.read_csv(file_path)

            if y in dataFrame.columns:
                for col in dataFrame.columns:
                    if col != y:
                        x_variable.append(col)

                dataFrame[x_variable]

                await ctx.send(f"```text\nData Contents:\n\n{dataFrame.to_markdown(index=False)}\n```")
            else:
                await ctx.send(f"The column '{y}' does not exist in the CSV file, {ctx.author}. You bitch!!")

        else:
            await ctx.send(f"This is not a csv file, {ctx.author}. You dumb fuck!!")

@bot.command()
async def Mindungie(ctx): #ctx = context
    print(ctx.author)
    print(ctx.channel)
    print(ctx.guild)
    await ctx.send("Wassap Bitch!!")

@bot.command()
async def yo(ctx): #ctx = context
    print(ctx.author)
    print(ctx.channel)
    print(ctx.guild)
    await ctx.send("Yahalloooooo")

@bot.command()
async def roll(ctx): #ctx = context
    number = random.randint(1,1000)
    await ctx.send(f"You rolled {number}")

bot.run(TOKEN)