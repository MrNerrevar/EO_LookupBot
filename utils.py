from enum import Enum, auto


class ItemType(Enum):
    General = 0
    Reserved = 1
    Currency = 2
    Heal = 3
    Teleport = 4
    Transformation = 5
    ExpReward = 6
    SkillBook = 7
    StatReset = 8
    Key = 9
    Weapon = 10
    Shield = 11
    Armor = 12
    Hat = 13
    Boots = 14
    Gloves = 15
    Accessory = 16
    Belt = 17
    Necklace = 18
    Ring = 19
    Armlet = 20
    Bracer = 21
    CosmeticArmor = 22
    CosmeticHat = 23
    CosmeticBack = 24
    CosmeticBuddyShoulder = 25
    CosmeticBuddyGround = 26
    CosmeticTorch = 27
    Alcohol = 28
    EffectPotion = 29
    HairDye = 30
    HairTool = 31
    CureCurse = 32
    TitleCertificate = 33
    VisualDocument = 34
    AudioDocument = 35
    TransportTicket = 36
    Fireworks = 37
    Explosive = 38
    Buff = 39
    Debuff = 40


class ItemSubType(Enum):
    none = 0
    Ranged = 1
    Arrows = 2
    Wings = 3
    Reserved4 = 4 #Potentially 2hander
    Quiver = 5


class ItemSpecial(Enum):
    Normal = 0
    Rare = 1
    Legendary = 2
    Unique = 3
    Lore = 4
    Cursed = 5

class NpcType(Enum):
    Friendly = 0
    Passive = 1
    Aggressive = 2
    Reserved3 = 3 #"pet" in the official pub editor
    Reserved4 = 4 #"npc mine" in the official pub editor
    Reserved5 = 5 #"npc killer" in the official pub editor
    Shop = 6
    Inn = 7
    Reserved8 = 8 #"locker" in the official pub editor
    Bank = 9
    Barber = 10
    Guild = 11
    Priest = 12
    Lawyer = 13
    Trainer = 14
    Quest = 15
