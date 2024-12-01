import os
import discord
import asyncio
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
#TOKEN = os.environ["DISCORD_TOKEN"]

intents = discord.Intents.default()
intents.message_content = True

# Initialize the bot with the command prefix and intents
bot = commands.Bot(command_prefix='/', intents=intents)

cogs_list = [
    'players',
    'items',
    'npcs'
]


def load_extensions():
    for cog in cogs_list:
        bot.load_extension(f'cogs.{cog}')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


# Error handling for app commands
async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send_message(f'You\'re on cooldown! Try again in {error.retry_after:.2f} seconds.',
                               ephemeral=True)
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send_message('You don\'t have permission to use this command.', ephemeral=True)
    else:
        await ctx.send_message('An error occurred. Please try again later.', ephemeral=True)
        print(f'An error occurred: {error}')


async def main():
    async with bot:
        if TOKEN is None:
            print('Error: DISCORD_TOKEN not found')
        else:
            await bot.start(TOKEN)

load_extensions()
asyncio.run(main())