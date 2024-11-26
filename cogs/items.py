
import discord
import asyncio
from discord.ext import commands
import requests
import os


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

    
    # ignore = ['id', 
    #         'name', 
    #         'graphic', 
    #         'item_type', 
    #         'item_sub_type', 
    #         'item_unique',
    #         'light',
    #         'dark',
    #         'earth',
    #         'air',
    #         'water'
    #         'fire',
    #         'spec1',
    #         'spec2',
    #         'spec3',
    #         'aoe_flag',
    #         'size',
    #         'drops',
    #         'craftables',
    #         'ingredientFor',
    #         'soldBy',
    #         'questRewards',
    #         'gatherableMaps',
    #         'gatherableSpots',
    #         'chestSpawnChests',
    #         'graphic_url'
    #         ]


    # def Process(json):
    #     for key, value in json.items():
    #         if key in ignore: continue
    #         try:
    #             if isinstance(value, dict):
    #                 Process(value)
    #             if isinstance(value, list):
    #                 for v in value:
    #                     Process(v)
    #             if int(value) > 0:
    #                 print(key, value)
    #         except:
    #             continue


    @discord.slash_command(name='item_lookup', description='Returns information about an item')
    async def item_lookup(self, ctx, item: str):
        items = self.fetch_all_items()

        if items:
            item = self.fetch_item_details(items, item)

            if item:
                print('Got details')
                print(item)
                print(item['name'])
                print([item['graphic_url']])

                await ctx.response.defer()
                # await asyncio.sleep(20)
                await ctx.followup(f'Item: {item['name']} found')

def setup(bot):  # this is called by Pycord to setup the cog
    bot.add_cog(Items(bot))
