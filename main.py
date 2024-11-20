import os
import discord
from discord import app_commands
from discord.ext import commands
import player_lookups as pl

intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with the command prefix and intents
bot = commands.Bot(command_prefix='/', intents=intents)

icon = discord.File("EO_Bot_Icon.png", filename=filename)

cogs_list = [
    'player_cog'
]

for cog in cogs_list:
    bot.load_extension(f'cogs.{cog}')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    try:
        synced = await bot.tree.sync()  # Sync app commands (slash commands) with Discord
        print(f'Synced {len(synced)} commands.')
    except Exception as e:
        print(f'Error syncing commands: {e}')


# Error handling for app commands
@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if isinstance(error, app_commands.CommandOnCooldown):
        await interaction.response.send_message(f'You\'re on cooldown! Try again in {error.retry_after:.2f} seconds.',
                                                ephemeral=True)
    elif isinstance(error, app_commands.MissingPermissions):
        await interaction.response.send_message('You don\'t have permission to use this command.', ephemeral=True)
    else:
        await interaction.response.send_message('An error occurred. Please try again later.', ephemeral=True)
        print(f'An error occurred: {error}')


# Run the bot with the token loaded from .env
bot.run(os.environ["DISCORD_TOKEN"], bot=True)
