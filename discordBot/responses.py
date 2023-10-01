import pandas as pd
from discord import Embed
from request import get_prices
import discord

df = pd.read_csv("/home/tier1marketspace/discordBot/newsletter.csv")

embed = Embed(title="7 Day Yu-Gi-Oh Top Movers")
embed.description = "Check sales history on TCGplayer for tcgDirect sales that may have skewed the market price."

def custom_title(s):
    return ' '.join([word[0].upper() + word[1:].lower() if word else '' for word in s.split()])

commands = {
    "!news": "Display the latest market report.",
    "!price": "Get prices for a Yu-Gi-Oh! card. Usage: !prices <Set Number> <days> <rarity (optional)>",
    "!help": "Display this list of commands.",
    "?!": "prefix for a private direct message."

}

for index, row in df.iterrows():
    card_info = (
        f"Set Number: {row['Set Number']}\n"
        f"Market Price: {row['Price (2)']}\n"
        f"Change ($): {row['Change ($)']}\n"
        f"Change (%): {row['Change (%)']}\n"
        f"[TCGplayer]({row['tcgplayerUrl']})"
    )
    embed.add_field(name=row['Name'], value=card_info, inline=False)

def get_response(user_message):
    p_message = user_message.lower()

    if p_message == "!help":
        help_msg = "Here are the available commands:\n"
        for cmd, desc in commands.items():
            help_msg += f"{cmd} - {desc}\n"
        return help_msg

    if p_message == "!news":
        return embed

    if p_message.startswith("!price"):

        parts = p_message.split(maxsplit=2)
        print(parts)


        if len(parts) < 3:
            return "Invalid !price command format. Expected format: '!price <product_id> <date_range> <rarity (optional)>'"

        command = parts[0]
        productId = parts[1]


        remaining_parts = parts[2].split()
        date_range = remaining_parts[0]
        productId = productId.upper()

        rarity = ' '.join(remaining_parts[1:]) if len(remaining_parts) > 1 else None


        if rarity:
            rarity = custom_title(rarity)


        if rarity:
            rarity = rarity.replace(' ', '%20')

        print(rarity)

        result = get_prices(productId, date_range, rarity)

        if result['type'] == 'pricing':
            discord_message = result['data']


            if 'png_path' in discord_message:
                embed2 = discord.Embed(
                    title=discord_message['name'],
                    description=f"[View on TCGplayer]({discord_message['tcgUrl']})",
                    color=0x00ff00
                )
                embed2.set_thumbnail(url=discord_message['imageUrl'])
                embed2.set_image(url="attachment://image.png")
                return (discord_message['png_path'], embed2)

        elif result['type'] == 'matching_numbers':
            df = result['data']
            print(df)
            embed_numbers = Embed(title="Multiple Rarities for One Set Number", description=f"Try your query again and specify rarity: !price {productId} {date_range} *Add Rarity Here*")
            for _, row in df.iterrows():
                embed_numbers.add_field(name=row['name'], value=f"Number: {row['number']}\nRarity: {row['rarity']}", inline=False)
            return embed_numbers



