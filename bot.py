import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

intents = discord.Intents.default()
intents.message_content = True  # Required for reading messages

bot = commands.Bot(command_prefix="c!", intents=intents)
tree = bot.tree  # Command tree for slash commands


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Sync slash commands on bot startup
    try:
        synced = await tree.sync()
        print(f"Synced {len(synced)} commands globally.")
    except Exception as e:
        print(f"Error syncing commands: {e}")


@bot.command()
async def ping(ctx):
    await ctx.send("Pong! **carib!** is online and ready to go!")


# Slash command
@tree.command(name="ping", description="Check bot response time")
async def ping_slash(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Pong! **carib!** is online and ready to go!")

keep_alive()

bot.run(TOKEN)
