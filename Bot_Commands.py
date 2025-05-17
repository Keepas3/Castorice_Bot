import os
import discord
from discord import app_commands
from discord import Embed
from discord.ext import commands

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
bot.run(TOKEN)