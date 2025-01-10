import discord
from discord.ext import commands


class PaginationView(discord.ui.View):
    current_page : int = 1
    sep : int = 10

    async def send(self, ctx):
        self.message = await ctx.send(view=self)
        await self.update_message(self.data[:self.sep])

    def create_embed(self, data):
        embed = discord.Embed(title="Guild Leaderboard", description=f"{self.current_page} / {int(len(self.data) / self.sep) + 1}")
        embed.add_field(name='Characters', 
                        value="\n".join(f"{name}" for name in data), 
                        inline=False)
        return embed

    async def update_message(self,data):
        self.update_buttons()
        await self.message.edit(embed=self.create_embed(data), view=self)

    def update_buttons(self):
        if self.current_page == 1:
            self.first_page_button.disabled = True
            self.prev_button.disabled = True
            self.first_page_button.style = discord.ButtonStyle.gray
            self.prev_button.style = discord.ButtonStyle.gray
        else:
            self.first_page_button.disabled = False
            self.prev_button.disabled = False
            self.first_page_button.style = discord.ButtonStyle.green
            self.prev_button.style = discord.ButtonStyle.primary

        if self.current_page == int(len(self.data) / self.sep) + 1:
            self.next_button.disabled = True
            self.last_page_button.disabled = True
            self.last_page_button.style = discord.ButtonStyle.gray
            self.next_button.style = discord.ButtonStyle.gray
        else:
            self.next_button.disabled = False
            self.last_page_button.disabled = False
            self.last_page_button.style = discord.ButtonStyle.green
            self.next_button.style = discord.ButtonStyle.primary

    def get_current_page_data(self):
        until_item = self.current_page * self.sep
        from_item = until_item - self.sep
        if not self.current_page == 1:
            from_item = 0
            until_item = self.sep
        if self.current_page == int(len(self.data) / self.sep) + 1:
            from_item = self.current_page * self.sep - self.sep
            until_item = len(self.data)
        return self.data[from_item:until_item]


    @discord.ui.button(label="|<", style=discord.ButtonStyle.green)
    async def first_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = 1

        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label="<", style=discord.ButtonStyle.primary)
    async def prev_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page -= 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">", style=discord.ButtonStyle.primary)
    async def next_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page += 1
        await self.update_message(self.get_current_page_data())

    @discord.ui.button(label=">|", style=discord.ButtonStyle.green)
    async def last_page_button(self, interaction:discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        self.current_page = int(len(self.data) / self.sep) + 1
        await self.update_message(self.get_current_page_data())


class Guilds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.icon_path = "images/EO_Bot_Icon.png"
        self.icon = "EO_Bot_Icon.png"

    @discord.slash_command(
        name="guild_list", description="Returns a list of Guild members"
    )
    async def guild_lookup(self, ctx):
        #await ctx.response.defer()

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

        pagination_view = PaginationView(timeout=None)
        pagination_view.data = member_names

        # guild = ctx.guild

        # for member in guild.members:
        #     if not member.bot:
        #         member_names.append(member.name)

        print("\n".join(member_names))

        #await ctx.followup.send("\n".join(member_names))
        await pagination_view.send(ctx)

def setup(bot):
    bot.add_cog(Guilds(bot))
