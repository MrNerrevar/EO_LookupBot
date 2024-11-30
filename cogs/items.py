
import discord
import asyncio
from discord.ext import commands
import requests
import os
from enums import ItemType, ItemSubType
from types import SimpleNamespace
from typing import Any, Union
from models.item_model import Item, map_item
from dataclasses import fields


class Items(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.icon_path = 'images/EO_Bot_Icon.png'
        self.icon = 'EO_Bot_Icon.png'


    def fetch_all_items(self):
        base_url = 'https://eor-api.exile-studios.com/api/items'
        response = requests.get(base_url)

        # Ensure response is valid
        if response.status_code == 200:
            data = response.json()
            return data.get('data', [])
        else:
            print(f'Failed to fetch data. Status code: {response.status_code}')
            return None

    
    def fetch_item_details(self, items, item_name):
        for item in items:
            if item['name'].lower() == item_name.lower():
                print(f'Item {item["name"]} found')

                item_url = item['url']
                print(item_url)
                item_response = requests.get(item_url)

                # Ensure response is valid
                if item_response.status_code == 200:
                    data = item_response.json()
                    return data
                else:
                    print(f'Failed to fetch data. Status code: {response.status_code}')
                    return None


    def get_item_description(self, item: Item) -> str:
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

        # Default output if no conditions are met
        return f'{item.item_type.name} Item'


    def get_item_attributes(self, item):
        attributes = {}
        # Iterate through all attributes of the item object
        for field in fields(item):
            attribute_name = field.name
            attribute_value = getattr(item, attribute_name)
            if attribute_value > 0:
                # Format the label (replace underscores with spaces and capitalize each word)
                formatted_label = attribute_name.replace("_", " ").title()

                attributes.update({formatted_label: attribute_value})
        
        return attributes

    
    def get_drop_npcs(self, item, drops):
        drop_npcs = []
        for drop in drops:
            print(drop['npc_url'])
            npc_url = drop['npc_url']
            response = requests.get(npc_url)

            # Ensure response is valid
            if response.status_code == 200:
                npc = response.json()
                print(npc['name'])
                drop_npcs.append(npc['name'])
            else:
                print(f'Failed to fetch data. Status code: {response.status_code}')
                return None
            
        return drop_npcs


    @discord.slash_command(name='item_lookup', description='Returns information about an item')
    async def item_lookup(self, ctx, item: str):
        await ctx.response.defer()
        # declaring icon as discord file (Required per command)
        icon = discord.File(self.icon_path, filename=self.icon)

        items = self.fetch_all_items()

        if items:
            item = map_item(self.fetch_item_details(items, item))

            print(item)
            if item:
                item_embed = discord.Embed(title=item.name,
                                            description=self.get_item_description(item),
                                            color=0x63037a)
                item_embed.set_author(name='Item Lookup',
                                            icon_url=f'attachment://EO_Bot_Icon.png')
                item_embed.set_thumbnail(url=item.graphic_url)

                if self.get_item_attributes(item.stats):
                    item_embed.add_field(name='Stats', 
                                        value='\n'.join(f'{key}: {value}' for key, value in self.get_item_attributes(item.stats).items()),
                                        inline=True)

                if self.get_item_attributes(item.requirements):
                    item_embed.add_field(name='Requirements', 
                                        value='\n'.join(f'{key}: {value}' for key, value in self.get_item_attributes(item.requirements).items()),
                                        inline=True)
                
                if item.drops:
                    drops = self.get_drop_npcs(item, item.drops)

                    #Needs to be fixed to show all NPCs, currently only last in the list
                    print(f'Drops: {drops}')
                    item_embed.add_field(name='Drops From', 
                                        value='\n'.join(f'{npc}' for npc in drops),
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

def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Items(bot))
