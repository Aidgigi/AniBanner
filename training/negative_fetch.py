import discord
from discord.ext.commands import Bot
import json
import sys
import asyncio

arg_pack = sys.argv[1:]

# instantiating the client
client = Bot(command_prefix=["!"], self_bot = True)

ran = False

attachments = []

@client.event
async def on_message(ctx):
    global ran, attachments
    print("1")
    if ctx.author.name == "Aidgigi" and ctx.channel.name == "off-topic" and not ran:
        ran = True

        async for message in ctx.channel.history(limit = None):
            if (atts := message.attachments):
                print(len(attachments))
                for att in atts:
                    attachments.append(att.url)
                
            if len(attachments) % 50 == 0:
                with open(arg_pack[1], "a") as f:
                    for att in attachments:
                        f.write(f"{att}\n")
            
                attachments = []
        
            

            



client.run(arg_pack[0], bot = False)

