import discord
import requests
from discord.ext import commands


class Guilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.icon_path = "images/EO_Bot_Icon.png"
        self.icon = "EO_Bot_Icon.png"


    def fetch_all_guilds(self):
        url = 'https://eodash.com/api/guilds'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data.get('guilds', [])
        else:
            error_message = f'Failed to fetch data. Status code: {response.status_code}'
            print(error_message)
            raise ValueError(error_message)


    @discord.slash_command(name='guilds', description='Returns a list of the top 10 guilds')
    async def guild_leaderboard(self, ctx):
        await ctx.response.defer()
        icon = discord.File(self.icon_path, filename=self.icon)

        guilds = self.fetch_all_guilds()[:10]

        try:
            ranks = ""
            tags = ""
            members = ""

            for guild in guilds:
                ranks += f"**{guild.get('rank', 'N/A')}**\n"
                tags += f"[{guild.get('tag', 'N/A')}] {guild.get('name', 'N/A')}\n"
                members += f"{guild.get('members', 'N/A')}\n"


            leaderboard_embed = discord.Embed(title='Top 10 Guilds', color=0x63037a)
            leaderboard_embed.set_author(name='Guilds Lookup',
                                        icon_url='attachment://EO_Bot_Icon.png')
            leaderboard_embed.set_thumbnail(url='attachment://EO_Bot_Icon.png')

            leaderboard_embed.add_field(name='Rank', value=ranks, inline=True)
            leaderboard_embed.add_field(name='Guild', value=tags, inline=True)
            leaderboard_embed.add_field(name='Members', value=members, inline=True)

            leaderboard_embed.set_footer(text='Provided by Nerrevar - Data pulled from EoDash')

            await ctx.followup.send(file=icon, embed=leaderboard_embed)
        except ValueError:
            failure_embed = discord.Embed(title='Lookup Failure',
                                            description='Failed to find the Guilds list',
                                            color=0x63037a)
            failure_embed.set_author(name='Guilds Lookup Lookup',
                                            icon_url='attachment://EO_Bot_Icon.png')
            await ctx.followup.send(file=icon, embed=failure_embed)


def setup(bot):
    bot.add_cog(Guilds(bot))
