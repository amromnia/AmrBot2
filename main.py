import random
import discord
from discord.ext import commands
from dotenv import dotenv_values
import shlex
import json
import logging
import argparse
import sys

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




def arg_handle():
    parser = argparse.ArgumentParser(description='Discord Bot')
    g = parser.add_mutually_exclusive_group()
    g.add_argument('--install', help='Initialize the bot and make required files', action='store_true')
    g.add_argument('--add-gif', help='Add a gif to the list of gifs', dest='add_gif_url')
    g.add_argument('--remove-gif', help='Remove a gif from the list of gifs', action='store_true')
    g.add_argument('--list-gifs', help='List all the gifs in the list of gifs', action='store_true')
    g.add_argument('--change-prefix', help='Change the command prefix')
    g.add_argument('--change-token', help='Change the discord bot token')

    args = parser.parse_args()
    add_gifs_url = args.add_gif_url

    if args.install:
        jsonFile = json.load(open('config.json'))
        jsonFile['commandPrefix'] = input("Enter the command prefix: ")
        # check if there are any gifs in the list
        if 'GIFList' not in jsonFile:
            jsonFile['GIFList'] = []
        # ask if they want to add more gifs, after initial stop at DONE
        gif_choice = input('Do you want to add more gifs? (y/n): ')
        if gif_choice == 'y':
            print("Enter 'DONE' to stop adding gifs")
            while True:
                gif = input("Enter the gif url: ")
                if gif == 'DONE':
                    break
                if gif not in jsonFile['GIFList']:
                    jsonFile['GIFList'].append(gif)
        # write to config.json
        with open('config.json', 'w') as f:
            json.dump(jsonFile, f, indent=4)

        # initialize .env file
        with open('.env', 'w') as f:
            discord_token = input("Enter the discord bot token: ")
            f.write(f"TOKEN={discord_token}")

    if args.add_gif_url:
        jsonFile = json.load(open('config.json'))
        # check if GIFList exists
        if 'GIFList' not in jsonFile:
            jsonFile['GIFList'] = []
        if add_gifs_url not in jsonFile['GIFList']:
            jsonFile['GIFList'].append(add_gifs_url)
        with open('config.json', 'w') as f:
            json.dump(jsonFile, f, indent=4)

    if args.remove_gif:
        # list all the gifs, then make a cursor to select the gif to remove
        jsonFile = json.load(open('config.json'))
        if 'GIFList' not in jsonFile:
            print("There are no gifs to remove")
            return
        for i, gif in enumerate(jsonFile['GIFList']):
            print(f"{i+1}. {gif}")
        #get all numbers inputted by user, separated by spaces
        gif_numbers = input("Enter the numbers of the gifs you want to remove separated by spaces: ")
        gif_numbers = gif_numbers.split(' ')
        # remove the gifs
        for gif_number in gif_numbers:
            jsonFile['GIFList'].pop(int(gif_number)-1)
        # write to config.json
        with open('config.json', 'w') as f:
            json.dump(jsonFile, f, indent=4)

    if args.list_gifs:
        jsonFile = json.load(open('config.json'))
        if 'GIFList' not in jsonFile:
            print("There are no gifs to list")
            return
        for i, gif in enumerate(jsonFile['GIFList']):
            print(f"{i+1}. {gif}")

    if args.change_prefix:
        jsonFile = json.load(open('config.json'))
        jsonFile['commandPrefix'] = args.change_prefix
        with open('config.json', 'w') as f:
            json.dump(jsonFile, f, indent=4)

    if args.change_token:
        with open('.env', 'w') as f:
            f.write(f"TOKEN={args.change_token}")


if __name__ == "__main__":
    arg_handle()
    # check for no arguments
    if len(sys.argv) == 1:
        main()