import random
import discord
from discord.ext import commands
from dotenv import dotenv_values
import shlex
import json
import logging

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)

handler = logging.FileHandler(filename='discordBot.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)


env = dotenv_values()
jsonFile = json.load(open('config.json'))


intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True

bot = commands.Bot(command_prefix=jsonFile['commandPrefix'], intents=intents)
gifList = jsonFile['GIFList']

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'Logged in as {bot.user}')

@bot.hybrid_command(name="burn", description="Burns whoever you want")
async def burn(ctx, names: str):
    names = names.replace('  ', ' ')
    names = names.replace(' ', ', ')
    if str(ctx.message.author.id) in names.lstrip():
        await ctx.send("No! Don't Burn Yourself!")
        return
    embed = discord.Embed(title="Burned", description=f"*{names} Burns With Fire!*", color=0xff0000)
    embed.set_image(url=random.choice(gifList))
    await ctx.send(embed=embed)

@bot.hybrid_command(name="kill", description="Kills whoever you want")
async def kill(ctx, names: str):
    await burn(ctx, names)

@bot.tree.command(name="roulette", description="Pick Randomly From A List")
async def roulette(ctx, list: str):
    list = shlex.split(list)
    await ctx.response.send_message(f":slot_machine: Roulette Has Chosen: **{random.choice(list)}** :slot_machine: ")

@bot.command(name="ping")
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")

@bot.command(name="roulette")
async def roulette(ctx, *args):
    await ctx.send(f":slot_machine: Roulette Has Chosen: **{random.choice(args)}** :slot_machine: ")

def main():
    bot.run(env['TOKEN'], reconnect=True, log_handler=handler, log_level=logging.INFO, log_formatter=logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))


if __name__ == "__main__":
    main()