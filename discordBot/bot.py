import discord
import responses
from discord import Embed

async def send_message(message, user_message, is_private):
    try:
        response = responses.get_response(user_message)
        if isinstance(response, tuple):  # Check if it's a tuple containing a file path and embed
            file_path, embed = response
            file = discord.File(file_path, filename="image.png")
            await message.author.send(file=file, embed=embed) if is_private else await message.channel.send(file=file, embed=embed)
        elif isinstance(response, Embed):
            await message.author.send(embed=response) if is_private else await message.channel.send(embed=response)
        else:
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def run_discord_bot():
    TOKEN = 'TOKEN HERE'
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
       print(f'{client.user} is now running!')

    @client.event
    async def on_message(message):
        if message.author == client.user:
            return

        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        print(f'{username} said: "{user_message}" ({channel})')

        if user_message[0] == '?':
            user_message = user_message[1:]
            await send_message(message, user_message, is_private=True)
        else:
            await send_message(message, user_message, is_private=False)

    client.run(TOKEN)