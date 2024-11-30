from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional
from enums import NpcType

# Data Models
@dataclass
class Stats:
    hp: int
    tp: int
    min_damage: int
    max_damage: int
    accuracy: int
    evasion: int
    armor: int
    critical_chance: int

@dataclass
class Drops:
    itemID: int
    drop_percent: int
    item_url: str = ""

@dataclass
class NPC:
    id: int
    name: str
    default_boundary: int
    graphic: int
    race: int
    boss: int
    child: int
    behavior: NpcType
    vendor_id: int
    greeting_sfx_id: int
    agro_sfx_id: int
    idle_sfx_id: int
    unk_sfx_id: int
    unk2_sfx_id: int
    unk3_sfx_id: int
    npc_respawn_secs: int
    npc_spawn_time: int
    npc_default_speed: int
    max_loaded_frames_flag: int
    max_loaded_frames: int
    alpha_normal_frames: int
    alpha_attack_frames: int
    courage: int
    move_flag: int
    move_blocked: int
    move_conveyor: int
    stats: Stats
    level: int
    experience: int
    drops: List[Drops] = field(default_factory=list)
    spawnMaps: int
    spawns: int
    respawn: str = ""
    graphic_url: str = ""