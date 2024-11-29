from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional
from enums import ItemType, ItemSubType

# Data Models
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
class Item:
    id: int
    name: str
    graphic: int
    item_type: ItemType  # Use the Enum
    item_sub_type: ItemSubType  # Use the Enum
    item_unique: int
    hp: int
    tp: int
    sp: int
    min_damage: int
    max_damage: int
    hit_rate: int
    evasion: int
    armor: int
    critical_chance: int
    power: int
    accuracy: int
    dexterity: int
    defense: int
    vitality: int
    aura: int
    light: int
    dark: int
    earth: int
    air: int
    water: int
    fire: int
    spec1: int
    spec2: int
    spec3: int
    required_level: int
    required_class: int
    required_power: int
    required_accuracy: int
    required_dexterity: int
    required_defense: int
    required_vitality: int
    required_aura: int
    weight: int
    range: int
    aoe_flag: int
    size: int
    sell_price: int
    drops: List[dict] = field(default_factory=list)
    craftables: List[Craftable] = field(default_factory=list)
    ingredientFor: List[dict] = field(default_factory=list)
    soldBy: List[dict] = field(default_factory=list)
    questRewards: List[dict] = field(default_factory=list)
    gatherableMaps: bool = False
    gatherableSpots: bool = False
    chestSpawnChests: bool = False
    graphic_url: str = ""

# Mapping Functions
def map_craft_ingredient(data: dict) -> CraftIngredient:
    return CraftIngredient(**data)

def map_craftable(data: dict) -> Craftable:
    craft_ingredients = [map_craft_ingredient(ing) for ing in data.get('craftIngredients', [])]
    return Craftable(
        shopName=data["shopName"],
        craftEon=data["craftEon"],
        craftGold=data["craftGold"],
        craftIngredients=craft_ingredients
    )

def map_item(data: dict) -> Item:
    craftables = [map_craftable(craft) for craft in data.get('craftables', [])]

    # Convert item_type and item_sub_type to Enum values
    item_type = ItemType(data["item_type"])
    item_sub_type = ItemSubType(data["item_sub_type"])

    return Item(
        id=data["id"],
        name=data["name"],
        graphic=data["graphic"],
        item_type=item_type,
        item_sub_type=item_sub_type,
        item_unique=data["item_unique"],
        hp=data["hp"],
        tp=data["tp"],
        sp=data["sp"],
        min_damage=data["min_damage"],
        max_damage=data["max_damage"],
        hit_rate=data["hit_rate"],
        evasion=data["evasion"],
        armor=data["armor"],
        critical_chance=data["critical_chance"],
        power=data["power"],
        accuracy=data["accuracy"],
        dexterity=data["dexterity"],
        defense=data["defense"],
        vitality=data["vitality"],
        aura=data["aura"],
        light=data["light"],
        dark=data["dark"],
        earth=data["earth"],
        air=data["air"],
        water=data["water"],
        fire=data["fire"],
        spec1=data["spec1"],
        spec2=data["spec2"],
        spec3=data["spec3"],
        required_level=data["required_level"],
        required_class=data["required_class"],
        required_power=data["required_power"],
        required_accuracy=data["required_accuracy"],
        required_dexterity=data["required_dexterity"],
        required_defense=data["required_defense"],
        required_vitality=data["required_vitality"],
        required_aura=data["required_aura"],
        weight=data["weight"],
        range=data["range"],
        aoe_flag=data["aoe_flag"],
        size=data["size"],
        sell_price=data["sell_price"],
        drops=data.get("drops", []),
        craftables=craftables,
        ingredientFor=data.get("ingredientFor", []),
        soldBy=data.get("soldBy", []),
        questRewards=data.get("questRewards", []),
        gatherableMaps=data.get("gatherableMaps", False),
        gatherableSpots=data.get("gatherableSpots", False),
        chestSpawnChests=data.get("chestSpawnChests", False),
        graphic_url=data["graphic_url"]
    )
