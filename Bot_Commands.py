import os
import discord
from discord import app_commands
from discord import Embed
from discord.ext import commands
import asyncio
import starrailcard
import asyncio
import io

from mihomo import Language, MihomoAPI
from mihomo.models import StarrailInfoParsed
from mihomo.models.v1 import StarrailInfoParsedV1
import requests

client = MihomoAPI(language=Language.EN)

#Retrieves the token from environment variables on your system
TOKEN = os.getenv("HSR_Bot")

#enables the bot to do certain things
intents = discord.Intents.default()
#enables the bot to receive messages
intents.messages = True  # Enable the message intent
#enables the bot to read the content of messages
intents.message_content = True
#enables the bot to read the presence of users (checks if their online/offline)
intents.presences = True  # Enable the presence intent

#The bot can read messages starting with ! as a command
bot = commands.Bot(command_prefix="!", intents=intents)



@bot.event
async def on_ready():
    await bot.tree.sync()
    await bot.change_presence(activity=discord.Game(name="with life"))
    print(f'logged in as {bot.user}!')

@bot.tree.command(name = "stats", description = "Get the stats of the bot")
async def stats(interaction: discord.Interaction):
    server_count = len(bot.guilds)
    user_count = len(bot.users)
    # embed = Embed(title="Bot Stats", color=0x00ff00)
    stats_message = (
        f"**Server Count:** {server_count}\n"
        f"**User Count:** {user_count}\n"
    )
    print(f"Bot Stats:\n{stats_message}")
    await interaction.response.send_message(stats_message)

@bot.tree.command(name = "ping", description = "Check the bot's latency")
async def ping(interaction: discord.Interaction):
    latency = bot.latency * 1000  # Convert to milliseconds
    print(f"Ping: {latency} ms")
    await interaction.response.send_message(f"Ping: {latency:.2f} ms")

# @bot.tree.command(name = "help", description = "Get a list of commands")
# async def help(interaction: discord.Interaction):
#     embed = Embed(title="Help", description="List of commands", color=0x00ff00)
#     embed.add_field(name="/stats", value="Get the stats of the bot", inline=False)
#     embed.add_field(name="/ping", value="Check the bot's latency", inline=False)
#     embed.add_field(name="/help", value="Get a list of commands", inline=False)
#     await interaction.response.send_message(embed=embed)

#Makes the bot run



# def get_player_data(uid):
#     url = f"https://api.mihomo.me/sr_info_parsed/{uid}?is_force_update=false"
#     headers = {"accept": "application/json"}  # Correct header format

#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         return response.json()  # Returns parsed JSON data
#     else:
#         print(f"Error: {response.status_code}")
#         return None

# # Example usage
# uid = "601619998"
# data = get_player_data(uid)

# if data:
#     print(data)  # Prints the retrieved JSON data



@bot.tree.command(name="profile", description="Get the stats of a player")
@app_commands.describe(uid="The UID of the player")
async def card(interaction: discord.Interaction, uid: str):
    url = f'https://api.mihomo.me/sr_info_parsed/{uid}?is_force_update=false'
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        await interaction.response.send_message("Error: Unable to fetch data.")
    if response.status_code == 200:
        # Parse the JSON response
        player_data = response.json()
        player_name = player_data['player']['nickname']
        player_uid = player_data['player']['uid']
        player_friends = player_data['player']['friend_count']
        player_level = player_data['player']['level']

        player_signature = player_data['player']['signature']
        player_character_count = player_data['player']['space_info']['avatar_count']
        player_lightcone_count = player_data['player']['space_info']['light_cone_count']
        player_achievements = player_data['player']['space_info']['achievement_count']
        player_relic_count = player_data['player']['space_info']['relic_count']

    data: StarrailInfoParsedV1 = await client.fetch_user_v1(uid)
    
    embed = discord.Embed(
        title=f"Profile of {player_name}",
        description= player_signature,
        color=0x00ff00
    )
    
    embed.set_thumbnail(url=client.get_icon_url(data.player.icon))  # Set profile avatar
    embed.add_field(name="🛡️ Clans", value="`/clanmembers` - View clan members\n`/claninfo` - Get clan details", inline=False)
    embed.add_field(name="⚔️ Players", value="`/playerinfo` - Get player stats\n`/playertroops` - View troop levels", inline=False)
    embed.add_field(name="📜 Misc", value="`/stats` - Bot statistics\n`/ping` - Check bot latency", inline=False)

    embed.set_footer(text="Use /command_name to execute a command.")

    
    if interaction.response.is_done():
        await interaction.followup.send(embed=embed)
    else:
        await interaction.response.send_message(embed=embed)




@bot.tree.command(name="card", description="Get the stats of a player")
@app_commands.describe(uid="The UID of the player")
async def card(interaction: discord.Interaction, uid: str):
    await interaction.response.defer()  # Prevent timeout

    data: StarrailInfoParsedV1 = await client.fetch_user_v1(uid)
    # async with starrailcard.Card() as card:
    #     card_data = await card.create(uid, style=2)  # Generate card

    # if not card_data:
    #     await interaction.followup.send("Error: Unable to generate card.")
    #     return
    embed = discord.Embed(
        title=f"Profile of {data.player.name}",
        color=0x00ff00
    )
    for character in data.characters:
        print(f"RELICS: {character.relics}")
        print(f" RELIC SETS: {character.relic_set.name}")
        # embed.add_field(
        #     name=f"{character.name} {character.rarity} ⭐ {character.relics}", 
            
        #     value=f"**Level:** {character.level} **Ediolons:**{character.eidolon}",
        #     inline=False
       # )
        
    await interaction.followup.send(embed=embed)


bot.run(TOKEN)