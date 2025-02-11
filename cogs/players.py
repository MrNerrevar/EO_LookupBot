# Player lookups are currently broken
# Due to Vult-r disabling relevant player data availability.
# Everything in here is now somewhat deprecated

import discord
import requests
from discord.ext import commands


class Players(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.icon_path = 'images/EO_Bot_Icon.png'
        self.icon = 'EO_Bot_Icon.png'


    def fetch_all_players(self):
        url = 'https://eodash.com/api/players'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data.get('players', [])
        else:
            error_message = f'Failed to fetch data. Status code: {response.status_code}'
            print(error_message)
            raise ValueError(error_message)

    def find_player_by_name(self, players, player_name):
        for player in players:
            if player['name'].lower() == player_name.lower():
                print(f'Player {player["name"]} found')
                return player

        error_message = f'Failed to find the specified player: {player_name}'
        print(error_message)
        raise ValueError(error_message)

    # Lookup a player and return their Name, rank and xp
    @discord.slash_command(name='player', description='Returns the Name, XP and leaderboard rank of a player')
    async def player_lookup(self, ctx, player: str):
        await ctx.response.defer()
        icon = discord.File(self.icon_path, filename=self.icon)
        players = self.fetch_all_players()

        try:
            player = self.find_player_by_name(players, player)

            if player:
                lookup_embed = discord.Embed(title=player['name'],
                                            description=f'Details of the player {player["name"]}',
                                            color=0x63037a)
                lookup_embed.set_author(name='Player Lookup',
                                            icon_url='attachment://EO_Bot_Icon.png')
                lookup_embed.set_thumbnail(url='attachment://EO_Bot_Icon.png')

                lookup_embed.add_field(name='Level', value=f'{player['level']}', inline=True)
                lookup_embed.add_field(name='Experience', value=f'{player['exp']:,}', inline=True)

                lookup_embed.add_field(name='Rank', value=f'{player['rank']}', inline=True)

                lookup_embed.set_footer(text='Provided by Nerrevar - Data pulled from EoDash')

            await ctx.followup.send(file=icon, embed=lookup_embed)
        except ValueError:
            failure_embed = discord.Embed(title='Lookup Failure',
                                            description='Failed to find the specified Player',
                                            color=0x63037a)
            failure_embed.set_author(name='Player Lookup',
                                            icon_url='attachment://EO_Bot_Icon.png')
            await ctx.followup.send(file=icon, embed=failure_embed)


    # Compare two players by xp and show the difference
    @discord.slash_command(name='player_compare', description='Compare two players by EXP and return the difference')
    async def player_compare(self, ctx, player1: str, player2: str):
        await ctx.response.defer()
        icon = discord.File(self.icon_path, filename=self.icon)
        players = self.fetch_all_players()

        try:
            player1 = self.find_player_by_name(players, player1)
            player2 = self.find_player_by_name(players, player2)

            if player1 and player2:
                compare_embed = discord.Embed(title='Exp Difference',
                                                description=f'Exp difference between {player1['name']} and {player2['name']}',
                                                color=0x63037a)
                compare_embed.set_author(name='Player Comparison',
                                                icon_url='attachment://EO_Bot_Icon.png')
                compare_embed.set_thumbnail(url='attachment://EO_Bot_Icon.png')

                compare_embed.add_field(name=f'{player1['name']}',
                                        value=f'Lvl: {player1['level']} - Exp: {player1['exp']:,}', inline=True)
                compare_embed.add_field(name=f'{player2['name']}',
                                        value=f'Lvl: {player2['level']} - Exp: {player2['exp']:,}', inline=True)

                if player1['exp'] > player2['exp']:
                    diff = player1['exp'] - player2['exp']
                    compare_embed.add_field(name='Difference',
                                            value=f'{player1['name']} has {diff:,} more experience than {player2['name']}',
                                            inline=False)
                elif player2['exp'] > player1['exp']:
                    diff = player2['exp'] - player1['exp']
                    compare_embed.add_field(name='Difference',
                                            value=f'{player2['name']} has {diff:,} more experience than {player1['name']}',
                                            inline=False)
                else:
                    compare_embed.add_field(name='No Difference',
                                            value='Miraculously, both players have the exact same amount of experience?!',
                                            inline=False)
            
                compare_embed.set_footer(text='Provided by Nerrevar - Data pulled from EoDash')

            await ctx.followup.send(file=icon, embed=compare_embed)
        except ValueError:
            failure_embed = discord.Embed(title='Lookup Failure',
                                            description='One or both of the players could not be found',
                                            color=0x63037a)
            failure_embed.set_author(name='Player Comparison',
                                            icon_url='attachment://EO_Bot_Icon.png')
            await ctx.followup.send(file=icon, embed=failure_embed)
            
def setup(bot):  
    bot.add_cog(Players(bot))
