import discord
from discord.ext.commands import Bot
import json
import sys
import asyncio

arg_pack = sys.argv[1:]

# instantiating the client
client = Bot(command_prefix=["!"])

ran = False

attachments = []

"""@client.event
async def on_ready():
    channel = client.get_channel("477962067677020171")
    print(channel.name)"""

@client.event
async def on_message(ctx):
    global ran, attachments
    if ctx.author.name == "Aidgigi" and ctx.channel.name == "off-topic" and not ran:
        ran = True
        num_found = 0

        async for message in ctx.channel.history(limit = None):
            if num_found >= int(arg_pack[1]):
                break

            if (atts := message.attachments):
                for att in atts:
                    num_found += 1
                    attachments.append(att.url)
                
            if len(attachments) % 50 == 0:
                print(num_found)
                with open(arg_pack[1], "a") as f:
                    for att in attachments:
                        f.write(f"{att}\n")
            
                attachments = []
        

client.run(arg_pack[0])

