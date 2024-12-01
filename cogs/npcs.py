import discord
from discord.ext import commands
import requests
from enums import NpcBehavior
from models.npc_model import Npc, map_npc
from dataclasses import fields


class Npcs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.icon_path = 'images/EO_Bot_Icon.png'
        self.icon = 'EO_Bot_Icon.png'


    def fetch_all_items(self):
        base_url = 'https://eor-api.exile-studios.com/api/npcs'
        response = requests.get(base_url)

        # Ensure response is valid
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            print(f'Failed to fetch data. Status code: {response.status_code}')
            return None


    def fetch_details(self, npcs, npc_name):
        for npc in npcs:
            if npc['name'].lower() == npc_name.lower():
                print(f'NPC {npc["name"]} found')

                npc_url = npc['url']
                print(npc_url)
                response = requests.get(npc_url)

                # Ensure response is valid
                if response.status_code == 200:
                    data = response.json()
                    return data
                else:
                    print(f'Failed to fetch data. Status code: {response.status_code}')
                    return None
                

    def get_attributes(self, npc):
        attributes = {}
        # Iterate through all attributes of the item object
        for field in fields(npc):
            attribute_name = field.name
            attribute_value = getattr(npc, attribute_name)
            if attribute_value > 0:
                # Format the label (replace underscores with spaces and capitalize each word)
                formatted_label = attribute_name.replace("_", " ").title()

                attributes.update({formatted_label: attribute_value})
        
        return attributes
    
    def get_drops(self, item, drops):
        drop_items = {}
        for drop in drops:
            print(drop['item_url'])
            item_url = drop['item_url']
            response = requests.get(item_url)

            # Ensure response is valid
            if response.status_code == 200:
                item = response.json()
                print(item['name'])
                drop_items.update({item['name']: drop['drop_percent']})
            else:
                print(f'Failed to fetch data. Status code: {response.status_code}')
                return None
            
        return drop_items

    @discord.slash_command(name='npc_lookup', description='Returns information about an npc')
    async def npc_lookup(self, ctx, npc: str):
        await ctx.response.defer()
        # declaring icon as discord file (Required per command)
        icon = discord.File(self.icon_path, filename=self.icon)

        npcs = self.fetch_all_items()

        if npcs:
            npc = map_npc(self.fetch_details(npcs, npc))

            print(npc)
            if npc:
                npc_embed = discord.Embed(title=npc.name,
                                            description='Placeholder',
                                            color=0x63037a)
                npc_embed.set_author(name='NPC Lookup',
                                            icon_url=f'attachment://EO_Bot_Icon.png')
                npc_embed.set_thumbnail(url=npc.graphic_url)


                if self.get_attributes(npc.stats):
                    npc_embed.add_field(name='Stats', 
                                        value='\n'.join(f'{key}: {value}' for key, value in self.get_attributes(npc.stats).items()),
                                        inline=True)

                if npc.drops:
                    npc_embed.add_field(name='Drops', 
                                        value='\n'.join(f'{item}: {percent}%' for item, percent in self.get_drops(npc, npc.drops).items()),
                                        inline=False)
                
                npc_embed.set_footer(text='Provided by Nerrevar - Data pulled from EOR-API')

            await ctx.followup.send(file=icon, embed=npc_embed)

def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Npcs(bot))
