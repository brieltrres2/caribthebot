import discord
from discord.ext import commands
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="c!", intents=intents)
tree = bot.tree  # For slash commands

# Temporary dictionary to store match schedules before confirmation
pending_schedules = {}

@tree.command(name="schedule", description="Schedule a match with an opponent's confirmation")
async def schedule(interaction: discord.Interaction, team_name: str, match_id: str, month: int, day: int, hour: int):
    # Retrieve opponent info from Google Sheets (you'll need to implement this part)
    opponent_team, opponent_captain_id = get_opponent_info(match_id)  # Placeholder function

    if not opponent_team or not opponent_captain_id:
        await interaction.response.send_message("Match ID not found or opponent data missing.", ephemeral=True)
        return

    schedule_message = (
        f"Match Scheduled!\n"
        f"**Team:** {team_name} vs {opponent_team}\n"
        f"**Match ID:** {match_id}\n"
        f"**Date:** {month}/{day} at {hour}:00\n"
        f"**Opponent Captain:** <@{opponent_captain_id}>\n"
        f"\nReact with ✅ to confirm the match within 10 minutes."
    )

    message = await interaction.response.send_message(schedule_message)
    message = await interaction.original_response()
    await message.add_reaction("✅")

    pending_schedules[message.id] = (interaction, opponent_captain_id)

    # Wait for reaction confirmation
    def check(reaction, user):
        return (
            reaction.message.id == message.id 
            and str(reaction.emoji) == "✅" 
            and user.id == opponent_captain_id
        )

    try:
        await bot.wait_for("reaction_add", timeout=600, check=check)  # 10 minutes timeout
        await interaction.followup.send("✅ Match successfully scheduled!")
        del pending_schedules[message.id]  # Remove from pending schedules
    except asyncio.TimeoutError:
        await interaction.followup.send("❌ Match scheduling cancelled due to no confirmation.")
        del pending_schedules[message.id]


def get_opponent_info(match_id):
    # Placeholder function for retrieving opponent details from Google Sheets
    # This should return (opponent_team, opponent_captain_id)
    return "Opponent Team", 123456789012345678  # Replace with real data

bot.run(TOKEN)
