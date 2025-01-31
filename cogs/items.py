
from dataclasses import fields

import discord
import requests
from discord.ext import commands

from enums import ItemSubType, ItemType
from models.item_model import Item, map_item


class Items(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.icon_path = 'images/EO_Bot_Icon.png'
        self.icon = 'EO_Bot_Icon.png'


    def fetch_all_items(self):
        base_url = 'https://eor-api.exile-studios.com/api/items'
        response = requests.get(base_url)
        
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            error_message = f'Failed to fetch data. Status code: {response.status_code}'
            print(error_message)
            raise ValueError(error_message)

    
    def fetch_details(self, items, item_name):
        for item in items:
            if item['name'].lower() == item_name.lower():
                print(f'Item {item["name"]} found')

                item_url = item['url']
                response = requests.get(item_url)

                if response.status_code == 200:
                    data = response.json()
                    return data
                else:
                    error_message = f'Failed to fetch data. Status code: {response.status_code}'
                    print(error_message)
                    raise ValueError(error_message)
                    
        error_message = f'Item {item_name} not found'
        print(error_message)
        raise ValueError(error_message)


    def get_item_type(self, item: Item) -> str:
        # If item_type is Weapon
        if item.item_type == ItemType.Weapon:
            if (item.item_sub_type == ItemSubType.Ranged) or int(item.stats.range > 0):
                return 'Ranged Weapon'
            else:
                return 'Melee Weapon'
        
        # If item_type is Shield (Back slot)
        if item.item_type == ItemType.Shield:
            if item.item_sub_type in {ItemSubType.Arrows, ItemSubType.Wings, ItemSubType.Quiver}:
                return item.item_sub_type.name  # Directly output the sub_type name
            else:
                return 'Shield'

        return f'{item.item_type.name} Item'


    def get_attributes(self, item):
        attributes = {}
        
        for field in fields(item):
            attribute_name = field.name
            attribute_value = getattr(item, attribute_name)
            if attribute_value > 0:
                formatted_label = attribute_name.replace("_", " ").title()
                attributes.update({formatted_label: attribute_value})
        
        return attributes

    
    def get_drops(self, item, drops):
        drop_npcs = {}
        for drop in drops:
            npc_url = drop['npc_url']
            response = requests.get(npc_url)

            if response.status_code == 200:
                npc = response.json()
                drop_npcs.update({npc['name']: drop['drop_percent']})
            else:
                error_message = f'Failed to fetch data. Status code: {response.status_code}'
                print(error_message)
                raise ValueError(error_message)
            
        return drop_npcs


    @discord.slash_command(name='item', description='Returns information about an item')
    async def item_lookup(self, ctx, item: str):
        await ctx.response.defer()

        icon = discord.File(self.icon_path, filename=self.icon)

        items = self.fetch_all_items()

        try:
            item = map_item(self.fetch_details(items, item))

            if item:
                item_embed = discord.Embed(title=item.name,
                                            description=self.get_item_type(item),
                                            color=0x63037a)
                item_embed.set_author(name='Item Lookup',
                                            icon_url='attachment://EO_Bot_Icon.png')
                item_embed.set_thumbnail(url=item.graphic_url)

                if self.get_attributes(item.stats):
                    item_embed.add_field(name='Stats', 
                                        value='\n'.join(f'{key}: {value}' for key, value in self.get_attributes(item.stats).items()),
                                        inline=True)

                if self.get_attributes(item.requirements):
                    item_embed.add_field(name='Requirements', 
                                        value='\n'.join(f'{key}: {value}' for key, value in self.get_attributes(item.requirements).items()),
                                        inline=True)
                
                if item.drops:
                    item_embed.add_field(name='Drops From', 
                                        value='\n'.join(f'{key}: {value}%' for key, value in self.get_drops(item, item.drops).items()),
                                        inline=False)

                if item.craftables:
                    item_embed.add_field(name='Craftable',
                                        value='Yes',
                                        inline=False)

                if item.sell_price > 0:
                    item_embed.add_field(name='Sell Price', 
                                        value=f'{item.sell_price} Eons',
                                        inline=False)

                item_embed.set_footer(text='Provided by Nerrevar - Data pulled from EOR-API')

            await ctx.followup.send(file=icon, embed=item_embed)
        except ValueError:
            failure_embed = discord.Embed(title='Lookup Failure',
                                            description='Failed to find the specified Item',
                                            color=0x63037a)
            failure_embed.set_author(name='Item Lookup',
                                            icon_url='attachment://EO_Bot_Icon.png')
            await ctx.followup.send(file=icon, embed=failure_embed)

def setup(bot):  
    bot.add_cog(Items(bot))
