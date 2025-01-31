# Currently unused
# Planned for use in a later refactor

from dataclasses import dataclass


@dataclass
class Guild:
    rank: int
    name: str
    tag: str
    members: int
    exp: int


def map_guild(data: dict) -> Guild:
    return Guild(
        rank=data['rank'],
        name=data['name'],
        tag=data['tag'],
        members=data['members'],
        exp=data['exp']
    )