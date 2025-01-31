from dataclasses import dataclass, field
from typing import List

from enums import ItemSubType, ItemType


@dataclass
class Stats:
    hp: int
    tp: int
    sp: int
    min_damage: int
    max_damage: int
    hit_rate: int
    range: int
    evasion: int
    armor: int
    critical_chance: int
    power: int
    accuracy: int
    dexterity: int
    defense: int
    vitality: int
    aura: int

@dataclass
class Elements:
    light: int
    dark: int
    earth: int
    air: int
    water: int
    fire: int

@dataclass
class Requirements:
    required_level: int
    required_class: int
    required_power: int
    required_accuracy: int
    required_dexterity: int
    required_defense: int
    required_vitality: int
    required_aura: int

@dataclass
class CraftIngredient:
    itemID: int
    quantity: int
    item_url: str

@dataclass
class Craftable:
    shopName: str
    craftEon: int
    craftGold: int
    craftIngredients: List[CraftIngredient]

@dataclass
class Drops:
    itemID: int
    drop_percent: int
    item_url: str = ''

@dataclass
class Item:
    id: int
    name: str
    graphic: int
    item_type: ItemType
    item_sub_type: ItemSubType
    item_unique: int
    stats: Stats
    elements: Elements
    requirements: Requirements
    spec1: int
    spec2: int
    spec3: int
    weight: int
    aoe_flag: int
    size: int
    sell_price: int
    drops: List[Drops] = field(default_factory=list)
    craftables: List[Craftable] = field(default_factory=list)
    ingredientFor: List[dict] = field(default_factory=list)
    soldBy: List[dict] = field(default_factory=list)
    questRewards: List[dict] = field(default_factory=list)
    gatherableMaps: bool = False
    gatherableSpots: bool = False
    chestSpawnChests: bool = False
    graphic_url: str = ''

def map_craft_ingredient(data: dict) -> CraftIngredient:
    return CraftIngredient(**data)

def map_craftable(data: dict) -> Craftable:
    craft_ingredients = [map_craft_ingredient(ing) for ing in data.get('craftIngredients', [])]
    return Craftable(
        shopName=data['shopName'],
        craftEon=data['craftEon'],
        craftGold=data['craftGold'],
        craftIngredients=craft_ingredients
    )

def map_drops(data: dict) -> Drops:
    return Drops(
        itemID=data['itemID'],
        drop_percent=data['drop_Percent'],
        item_url=data['item_url']
    )

def map_item(data: dict) -> Item:
    craftables = [map_craftable(craft) for craft in data.get('craftables', [])]

    # Convert item_type and item_sub_type to Enum values
    item_type = ItemType(data['item_type'])
    try:
        item_sub_type = ItemSubType(data['item_sub_type'])
    except ValueError:
        item_sub_type = None  # Ignore invalid subtypes

    stats = Stats(
        hp=data['hp'],
        tp=data['tp'],
        sp=data['sp'],
        min_damage=data['min_damage'],
        max_damage=data['max_damage'],
        hit_rate=data['hit_rate'],
        range=data['range'],
        evasion=data['evasion'],
        armor=data['armor'],
        critical_chance=data['critical_chance'],
        power=data['power'],
        accuracy=data['accuracy'],
        dexterity=data['dexterity'],
        defense=data['defense'],
        vitality=data['vitality'],
        aura=data['aura']
    )

    elements = Elements(
        light=data['light'],
        dark=data['dark'],
        earth=data['earth'],
        air=data['air'],
        water=data['water'],
        fire=data['fire']
    )

    requirements = Requirements(
        required_level=data['required_level'],
        required_class=data['required_class'],
        required_power=data['required_power'],
        required_accuracy=data['required_accuracy'],
        required_dexterity=data['required_dexterity'],
        required_defense=data['required_defense'],
        required_vitality=data['required_vitality'],
        required_aura=data['required_aura']
    )

    return Item(
        id=data['id'],
        name=data['name'],
        graphic=data['graphic'],
        item_type=item_type,
        item_sub_type=item_sub_type,
        item_unique=data['item_unique'],
        stats=stats,
        elements=elements,
        requirements=requirements,
        spec1=data['spec1'],
        spec2=data['spec2'],
        spec3=data['spec3'],
        weight=data['weight'],
        aoe_flag=data['aoe_flag'],
        size=data['size'],
        sell_price=data['sell_price'],
        drops=data.get('drops', []),
        craftables=craftables,
        ingredientFor=data.get('ingredientFor', []),
        soldBy=data.get('soldBy', []),
        questRewards=data.get('questRewards', []),
        gatherableMaps=data.get('gatherableMaps', False),
        gatherableSpots=data.get('gatherableSpots', False),
        chestSpawnChests=data.get('chestSpawnChests', False),
        graphic_url=data['graphic_url']
    )
