
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
            if (item.item_sub_type == ItemSubType.Ranged) or int(item.range > 0):
                return "Ranged Weapon"
            else:
                return "Melee Weapon"
        
        # If item_type is Shield (Back slot)
        if item.item_type == ItemType.Shield:
            if item.item_sub_type in {ItemSubType.Arrows, ItemSubType.Wings, ItemSubType.Quiver}:
                return item.item_sub_type.name  # Directly output the sub_type name
            else:
                return "Shield"

        # Default output if no conditions are met
        return "Unknown Item"


    @discord.slash_command(name='item_lookup', description='Returns information about an item')
    async def item_lookup(self, ctx, item: str):
        await ctx.response.defer()
        # declaring icon as discord file (Required per command)
        icon = discord.File(self.icon_path, filename=self.icon)

        items = self.fetch_all_items()

        ignore = [
            'id', 
            'name', 
            'graphic',
            'item_type', 
            'item_sub_type'
            'item_unique'
            'light',
            'dark',
            'earth',
            'air',
            'water'
            'fire',
            'spec1',
            'spec2',
            'spec3',
            'aoe_flag',
            'size',
            'drops',
            'craftables',
            'ingredientFor',
            'soldBy',
            'questRewards',
            'gatherableMaps',
            'gatherableSpots',
            'chestSpawnChests',
            'graphic_url'
            ]

        stats = [
            'hp',
            'tp',
            'sp',
            'min_damage',
            'max_damage',
            'hit_rate',
            'evasion',
            'armor',
            'critical_chance',
            'power',
            'accuracy',
            'dexterity',
            'defense',
            'vitality',
            'aura'
            ]

        requirements = [
            'required_level',
            'required_class',
            'required_power',
            'required_accuracy',
            'required_dexterity',
            'required_defense',
            'required_vitality',
            'required_aura'
            ]
        
        misc = [
            'sell_price'
        ]

        if items:
            item = map_item(self.fetch_item_details(items, item))

            if item:
                item_embed = discord.Embed(title=item.name,
                                            description=self.get_item_description(item),
                                            color=0x63037a)
                item_embed.set_author(name='Item Lookup',
                                            icon_url=f'attachment://EO_Bot_Icon.png')
                item_embed.set_thumbnail(url=item.graphic_url)

                # Iterate through all attributes of the item object
                for field in fields(item):
                    attribute_name = field.name
                    attribute_value = getattr(item, attribute_name)
                    # Format the label (replace underscores with spaces and capitalize each word)
                    formatted_label = attribute_name.replace("_", " ").title()

                    print(f"{formatted_label}: {attribute_value}")

                    if attribute_name in ignore:
                        continue
                    if attribute_name in stats:
                        if (attribute_value is int) and (attribute_value > 0):
                            print(f"{formatted_label}: {attribute_value}")
                    if attribute_name in requirements:
                        if (attribute_value is int) and (attribute_value > 0):
                            print(f"{formatted_label}: {attribute_value}")
                    if attribute_name in misc:
                        if (attribute_value is int) and (attribute_value > 0):
                            print(f"{formatted_label}: {attribute_value}")

                # Accessing properties
                # print(f'Name: {item.name}')  # Poison Quiver
                # print(f'Shop: {item.craftables[0].shopName}')  # Paul Pan Ranger Shop
                # print(f'URL: {item.craftables[0].craftIngredients[1].item_url}')
                # Output: https://eor-api.exile-studios.com/api/items/210

                item_embed.set_footer(text='Provided by Nerrevar - Data pulled from EOR-API')

            await ctx.followup.send(file=icon, embed=item_embed)

def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Items(bot))
