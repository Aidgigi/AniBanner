from discord.ext.commands import Bot
import discord
import uuid, requests, base64, os, random
import numpy as np

from tensorflow.keras.preprocessing import image

import tensorflow as tf

from PIL import Image

# preparing the tf model
model = tf.keras.models.load_model("./trained_model")

client = Bot(command_prefix = ["!"])

tf.saved_model.LoadOptions(
    experimental_io_device = '/physical_device:CPU'
)

allowed_channels = (854627368643592207, 855306527484542976, 855309516580061207)

def auto_uuid():
    return str(base64.urlsafe_b64encode(uuid.uuid1().bytes)).replace('=', '')[:-1:][2::]

def fetch_gradient(url):
    img = requests.get(url).content

    fname = f"{auto_uuid()}.jpg"

    with open(fname, 'wb') as f:
        f.write(img)

    img = image.load_img(fname, target_size = (224, 224))
    img = image.img_to_array(img)
    img = np.expand_dims(img, axis = 0)

    os.remove(fname)

    return model.predict(img, batch_size = 10)[0][0]

def gif_gradients(url):
    img = requests.get(url).content

    fname = f"{auto_uuid()}.gif"

    with open(fname, 'wb') as f:
        f.write(img)

    img = Image.open(fname)

    os.remove(fname)

    start = 0
    end = img.n_frames - 1
    rand = random.randrange(start, end)

    grads = []

    for selector in (start, end, rand):
        img.seek(selector)
        img2 = img.convert('RGB')
        fname = f"{auto_uuid()}.jpg"
        img2.save(fname)

        img2 = image.load_img(fname, target_size = (224, 224))
        img2 = image.img_to_array(img2)
        img2 = np.expand_dims(img2, axis = 0)

        os.remove(fname)

        grads.append(model.predict(img2, batch_size = 10)[0][0])

    return max(grads)

@client.event
async def on_ready():
    await client.change_presence(activity = discord.Game(name = "Aidgigi's Bitch Simulator 2021"))

@client.event
async def on_message(ctx):
    if (atts := ctx.attachments) and ctx.channel.id in allowed_channels:
        print(atts)
        for att in atts:
            if (ending := (url := att.url).lower().split('.')[-1]) not in ['jpg', 'jpeg', 'png']:
                if ending == 'gif':
                    grad = gif_gradients(url)

            grad = fetch_gradient(url)
            message = "Anime" if grad > 4.5 else "Not anime"

            await ctx.reply(message + f"\n\n{grad}", mention_author = False)


@client.event
async def on_raw_reaction_add(ctx):
    if (chan := ctx.channel_id) in allowed_channels:
        await client.get_channel(chan).send("reaction found")


with open("token", 'r') as f:
    TOKEN = f.read()

client.run(TOKEN)