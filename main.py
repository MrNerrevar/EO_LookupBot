import os
import discord
from discord import app_commands
from discord.ext import commands
import player_lookups as pl

intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with the command prefix and intents
bot = commands.Bot(command_prefix='/', intents=intents)

icon = discord.File("EO_Bot_Icon.png", filename="EO_Bot_Icon.png")


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    try:
        synced = await bot.tree.sync()  # Sync app commands (slash commands) with Discord
        print(f'Synced {len(synced)} commands.')
    except Exception as e:
        print(f'Error syncing commands: {e}')


# Lookup a player and return their Name, rank and xp
@bot.tree.command(name='lookup', description='Returns the Name, XP and leaderboard rank of a player')
@app_commands.describe(player='The player to lookup')
async def lookup(interaction: discord.Interaction, player: str):
    player_return = pl.print_player_info(player)

    lookup_embed=discord.Embed(title=player_return[0], 
                    description=f'Details of the player {player_return[0]}', 
                    color=0x63037a)
    lookup_embed.set_thumbnail(url="attachment://EO_Bot_Icon.png")

    lookup_embed.add_field(name='Level', value=f'{player_return[1]}', inline=True)
    lookup_embed.add_field(name='Experience', value=f'{player_return[2]:,}', inline=True)

    lookup_embed.add_field(name='Rank', value=f'{player_return[3]}', inline=True)

    lookup_embed.set_footer(text="Provided by Nerrevar")

    await interaction.response.send_message(file=icon, embed=lookup_embed)


# Compare two players by xp and show the difference
@bot.tree.command(name='compare', description='Compare two players by EXP and return the difference')
@app_commands.describe(player1='First player to check', player2='Second player to check')
async def compare(interaction: discord.Interaction, player1: str, player2: str):
    compare_return = pl.compare_players(player1, player2)

    compare_embed = discord.Embed(title='Exp Difference',
                        description=f'Exp difference between {compare_return[0]} and {compare_return[2]}',
                        color=0x63037a)
    compare_embed.set_thumbnail(url="attachment://EO_Bot_Icon.png")

    compare_embed.add_field(name=f'{compare_return[0]}', value=f'{compare_return[1]:,}', inline=True)
    compare_embed.add_field(name=f'{compare_return[2]}', value=f'{compare_return[3]:,}', inline=True)

    if compare_return[1] > compare_return[3]:
        diff = compare_return[1] - compare_return[3]
        compare_embed.add_field(name='Difference', value=f'{compare_return[0]} has {diff:,} more experience than {compare_return[2]}', inline=False)
    elif compare_return[3] > compare_return[1]:
        diff = compare_return[3] - compare_return[1]
        compare_embed.add_field(name='Difference', value=f'{compare_return[2]} has {diff:,} more experience than {compare_return[0]}', inline=False)
    else:
        compare_embed.add_field(name='No Difference', value='Miraculously, both players have the exact same amount of experience?!', inline=False)
    
    compare_embed.set_footer(text="Provided by Nerrevar")

    await interaction.response.send_message(file=icon, embed=compare_embed)


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
bot.run(os.environ["DISCORD_TOKEN"])
