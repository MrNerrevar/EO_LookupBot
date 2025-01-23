import json

import discord
import requests
from discord.ext import commands
from discord.ext.pages import Page, Paginator


class Guilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.icon_path = "images/EO_Bot_Icon.png"
        self.icon = "EO_Bot_Icon.png"

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

    def process_member_list(self, lookup_names, output_file):
        players = self.fetch_all_players()
        
        member_list = []
        for member in lookup_names:
            player = self.find_player_by_name(players, member)

            if player:
                member_list.append(player)

            with open(output_file, "w") as f:
                json.dump(member_list, f, indent=4)

            print(f"Filtered data saved to {output_file}")
            

    @discord.slash_command(name="guild_list", description="Returns a list of Guild members")
    async def guild_lookup(self, ctx):
        await ctx.response.defer()
        icon = discord.File(self.icon_path, filename=self.icon)

        member_names = [
            "Nerrevar",
            "Headhunter",
            "Jaiden",
            "Nick",
            "Kerosene",
            "Sizzle",
            "WillowP",
            "BillowD",
            "Mingle",
            "Living",
            "Recovery",
            "Mantelis",
            "Ronofa",
            "Babybear",
            "Shera",
            "Sequoia",
            "Ganstaboo",
            "Aquat",
            "Gretos",
            "Kellzkay",
            "Trippie",
            "Athlena",
            "Drommels",
            "Ethereal",
            "Gibby",
        ]

        self.process_member_list(member_names, 'members.json')
        # guild = ctx.guild

        # for member in guild.members:
        #     if not member.bot:
        #         member_names.append(member.name)

        print("\n".join(member_names))

        split_size = 10 

        splits = [member_names[i:i + split_size] for i in range(0, len(member_names), split_size)]

        leaderboard_pages = []
        #embeds = []
        # Example: Process each chunk (e.g., print or apply some operations)
        for split, names in enumerate(splits, start=1):
            #print(f"Processing Chunk {idx}: {split}")
            leaderboard_embed = discord.Embed(title=f'Page {split}', color=0x63037a)
            leaderboard_embed.set_author(name='Guild Leaderboard',
                                        icon_url='attachment://EO_Bot_Icon.png')
            leaderboard_embed.set_thumbnail(url='attachment://EO_Bot_Icon.png')

            leaderboard_embed.add_field(name='Rank', value='testrank', inline=True)
            leaderboard_embed.add_field(name='Name', value='\n'.join(f'{names}' for name in names), inline=True)
            leaderboard_embed.add_field(name='Level', value='testlevel', inline=True)

            leaderboard_embed.set_footer(text='Provided by Nerrevar - Data pulled from EoDash')

            #embeds.append(leaderboard_embed)
            leaderboard_pages.append(Page(embeds=[leaderboard_embed], files=[icon]))

        #await ctx.followup.send("\n".join(member_names))

        leaderboard = Paginator(pages=leaderboard_pages)
        await leaderboard.respond(ctx.interaction)
        #await ctx.followup.send(file=icon, Paginator=leaderboard)

def setup(bot):
    bot.add_cog(Guilds(bot))
