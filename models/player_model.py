# Highly unnecessary addition. And currently entirely unused.
# Mostly added in hope that Vult-r will re-enable player data availability.
# Player lookups are broken otherwise.

from dataclasses import dataclass


@dataclass
class Player:
    rank: int
    name: str
    level: int
    exp: int
    movement: str
    position: int