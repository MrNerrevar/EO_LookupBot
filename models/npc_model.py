from dataclasses import dataclass, field
from typing import List

from enums import NpcBehavior


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
class Info:
    level: int
    experience: int
    spawnMaps: int
    respawn: str = ''

@dataclass
class Drops:
    itemID: int
    drop_percent: int
    item_url: str = ''

@dataclass
class Npc:
    id: int
    name: str
    default_boundary: int
    graphic: int
    race: int
    boss: int
    child: int
    behavior: NpcBehavior
    vendor_id: int
    greeting_sfx_id: int
    agro_sfx_id: int
    idle_sfx_id: int
    attack_sfx_id: int
    walk_sfx_id: int
    alert_sfx_id: int
    npc_respawn_secs: int
    npc_spawn_time: int
    npc_default_speed: int
    max_loaded_frames_flag: int
    max_loaded_frames: int
    alpha_normal_frames: int
    alpha_attack_frames: int
    move_flag: int
    move_blocked: int
    move_conveyor: int
    stats: Stats
    info: Info
    spawns: int
    drops: List[Drops] = field(default_factory=list)
    graphic_url: str = ''

def map_drops(data: dict) -> Drops:
    return Drops(
        itemID=data['itemID'],
        drop_percent=data['drop_Percent'],
        item_url=data['item_url']
    )

def map_npc(data: dict) -> Npc:
    behavior = NpcBehavior(data['behavior'])

    stats = Stats(
        hp=data['hp'],
        tp=data['tp'],
        min_damage=data['min_damage'],
        max_damage=data['max_damage'],
        accuracy=data['accuracy'],
        evasion=data['evasion'],
        armor=data['armor'],
        critical_chance=data['critical_chance']
    )

    info = Info(
        level=data['level'],
        experience=data['experience'],
        spawnMaps=data['spawnMaps'],
        respawn=data['respawn']
    )

    return Npc(
        id=data['id'],
        name=data['name'],
        default_boundary=data['default_boundary'],
        graphic=data['graphic'],
        race=data['race'],
        boss=data['boss'],
        child=data['child'],
        behavior=behavior,
        vendor_id=data['vendor_id'],
        greeting_sfx_id=data['greeting_sfx_id'],
        agro_sfx_id=data['agro_sfx_id'],
        idle_sfx_id=data['idle_sfx_id'],
        attack_sfx_id=data['attack_sfx_id'],
        walk_sfx_id=data['walk_sfx_id'],
        alert_sfx_id=data['alert_sfx_id'],
        npc_respawn_secs=data['npc_respawn_secs'],
        npc_spawn_time=data['npc_spawn_time'],
        npc_default_speed=data['npc_default_speed'],
        max_loaded_frames_flag=data['max_loaded_frames_flag'],
        max_loaded_frames=data['max_loaded_frames'],
        alpha_normal_frames=data['alpha_normal_frames'],
        alpha_attack_frames=data['alpha_attack_frames'],
        move_flag=data['move_flag'],
        move_blocked=data['move_blocked'],
        move_conveyor=data['move_conveyor'],
        stats=stats,
        info=info,
        spawns=data['spawns'],
        drops=data.get('drops', []),
        graphic_url=data['graphic_url']
    )