
import discord
import asyncio
from discord.ext import commands
import requests
import os
from utils import ItemType, ItemSubType


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


    @discord.slash_command(name='item_lookup', description='Returns information about an item')
    async def item_lookup(self, ctx, item: str):
        await ctx.response.defer()
        items = self.fetch_all_items()

        ignore = [
            'id', 
            'name', 
            'graphic',
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

        types = [
            'item_type', 
            'item_sub_type'
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
            'aura',
            'light',
            'dark',
            'earth',
            'air',
            'water',
            'fire',
            'spec1',
            'spec2',
            'spec3'
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

        if items:
            item = self.fetch_item_details(items, item)

            item_types = {}
            item_stats = {}
            item_requirements = {}

            if item:
                for key, value in item.items():
                    if key in ignore: continue
                    try:
                        if isinstance(value, dict):
                            continue
                        if isinstance(value, list):
                            continue
                        if (key in types) and (int(value) > 0):
                            item_types.update({key: value})
                        if (key in stats) and (int(value) > 0):
                            item_stats.update({key.replace("_", " ").title(): value})
                        if (key in requirements) and (int(value) > 0):
                            item_requirements.update({key: value})
                    except:
                        continue

                # if (int(item_types['Item Sub Type']) > 0):
                #     if (int(item_types['Item Sub Type']) == 1):
                #         item_description = f'item_type'

                item_types.update({'item_type': ItemType(item_types['item_type']).name})
                item_types.update({'item_sub_type': ItemSubType(item_types['item_sub_type']).name})

                
                item_embed = discord.Embed(title=item['name'],
                                            description=f'{item_types}',
                                            color=0x63037a)
                item_embed.set_thumbnail(url=f'{item['graphic_url']}')

                if item_stats:
                    item_embed.add_field(name='Stats', 
                                                value='\n'.join(f'{key.replace("_", " ").title()}: {value}' for key, value in item_stats.items()))
                if item_requirements:    
                    item_embed.add_field(name='Requirements', 
                                                value='\n'.join(f'{key.replace("_", " ").title()}: {value}' for key, value in item_requirements.items()))

                item_embed.set_footer(text='Provided by Nerrevar - Data pulled from EOR-API')
            # await asyncio.sleep(20)
            await ctx.followup.send(embed=item_embed)

def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Items(bot))
