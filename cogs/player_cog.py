import discord
from discord import commands
import requests

class Player_Cog(commands.Cog):

    icon = discord.File('EO_Bot_Icon.png', filename='EO_Bot_Icon.png')

    
    def __init__(self, bot):
        self.bot = bot


    async def fetch_all_players():
        url = 'https://eodash.com/api/players'
        response = requests.get(url)

        # Ensure response is valid
        if response.status_code == 200:
            data = response.json()
            return data.get('players', [])
        else:
            print(f'Failed to fetch data. Status code: {response.status_code}')
            return None


    async def find_player_by_name(players, player_name):
        for player in players:
            if player.get('name', '').lower() == player_name.lower():
                return player
            else:
                print(f'Failed to find the specified player: {player_name}')
                return None


    # Lookup a player and return their Name, rank and xp
    @bot.tree.command(name='lookup', description='Returns the Name, XP and leaderboard rank of a player')
    @app_commands.describe(player='The player to lookup')
    async def lookup(self, ctx, player: str):
        players = fetch_all_players()

        if players:
            player = find_player_by_name(players, player_name)

            if player:
                lookup_embed=discord.Embed(title=player['name'],
                    description=f'Details of the player {player['name']}',
                    color=0x63037a)
                lookup_embed.set_thumbnail(url=f'attachment://{filename}')

                lookup_embed.add_field(name='Level', value=f'{player['level']}', inline=True)
                lookup_embed.add_field(name='Experience', value=f'{player.get['exp', 0]:,}', inline=True)

                lookup_embed.add_field(name='Rank', value=f'{player['rank']}', inline=True)
            else:
                lookup_embed=discord.Embed(title='ERROR',
                    description=f'Could not find the player {player['name']}',
                    color=0x7a0303)
                lookup_embed.set_thumbnail(url=f'attachment://{filename}')
            
            lookup_embed.set_footer(text='Provided by Nerrevar - Data pulled from EoDash')

        await ctx.respond(file=icon, embed=lookup_embed)


    # Compare two players by xp and show the difference
    @bot.tree.command(name='compare', description='Compare two players by EXP and return the difference')
    @app_commands.describe(player1='First player to check', player2='Second player to check')
    async def compare(self, ctx, player1: str, player2: str):
        players = fetch_all_players()

        if players:
            player1 = find_player_by_name(players, player1)
            player2 = find_player_by_name(players, player2)

            if player1 and player2:
                compare_embed = discord.Embed(title='Exp Difference',
                                    description=f'Exp difference between {player1['name']} and {player2['name']}',
                                    color=0x63037a)
                compare_embed.set_thumbnail(url=f"attachment://{filename}")

                compare_embed.add_field(name=f'{player1['name']}', value=f'Lvl: {player1['level']} - Exp: {player1.get('exp', 0):,}', inline=True)
                compare_embed.add_field(name=f'{player2['name']}', value=f'Lvl: {player2['level']} - Exp: {player2.get('exp', 0):,}', inline=True)

                if player1.get('exp', 0) > player2.get('exp', 0):
                    diff = player1.get('exp', 0) - player2.get('exp', 0)
                    compare_embed.add_field(name='Difference', value=f'{player1['name']} has {diff:,} more experience than {player2['name']}', inline=False)
                elif player2.get('exp', 0) > player1.get('exp', 0):
                    diff = player2.get('exp', 0) - player1.get('exp', 0)
                    compare_embed.add_field(name='Difference', value=f'{player2['name']} has {diff:,} more experience than {player1['name']}', inline=False)
                else:
                    compare_embed.add_field(name='No Difference', value='Miraculously, both players have the exact same amount of experience?!', inline=False)
            else:
                compare_embed = discord.Embed(title='Exp Difference',
                                    description=f'One or both of the players could not be found',
                                    color=0x7a0303)
                compare_embed.set_thumbnail(url=f"attachment://{filename}")
            
            lookup_embed.set_footer(text='Provided by Nerrevar - Data pulled from EoDash')

        await ctx.respond(file=icon, embed=compare_embed)

    def setup(bot): # this is called by Pycord to setup the cog
        bot.add_cog(Player_Cog(bot))