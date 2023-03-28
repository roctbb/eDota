import imp
import random
import sys

from domain.items.flag import FlagRed
from domain.items.flag import FlagBlue
from domain.items.coin import Coin
from domain.items.healthkit import HealthKit
from domain.items.sniper import SniperBooster
from domain.map import Map
from domain.game import Game
from domain.common import Position, Point, Direction
from domain.objects.Snow import Snow
from domain.objects.ancients import RadientAncient, DareAncient
from domain.objects.road import Road
from domain.objects.rocks import Rocks
from domain.objects.stump import Stump
from domain.objects.tree import Tree
from domain.objects.wall import Wall
from domain.objects.hardwall import HardWall
from domain.objects.water import Water
from domain.player import Player
from domain.repositories.players import PlayersRepository
from domain.units.tower import Tower

TEMPLATE = """
hhhhhhhhhhhhhhhhhhhhhh
tkk................kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk................kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk......kkkk......kkt
tkk.....kkkkkk.....kkt
t.s.......kk.......s.t
t.s.......kk.......s.t
tkk.....kkkkkk.....kkt
tkk......kkkk......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
tkk................kkt
tkk.......kk.......kkt
tkk.......kk.......kkt
hhhhhhhhhhhhhhhhhhhhhh
""".strip('\n')

BACKGROUND = """      
......................
.rr.......rr.......rr.
.rr...rrrrrrrrrr...rr.
.rr....rrrrrrrr....rr.
.rr...rr..rr..rr...rr.
.rr..rr...rr...rr..rr.
.rr.rr....rr....rr.rr.
.rrrr.....rr.....rrrr.
.rrr......rr......rrr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr......rrrr......rr.
.rr.....rrrrrr.....rr.
wwwwwwwwwwrrwwwwwwwwww
wwwwwwwwwwrrwwwwwwwwww
.rr.....rrrrrr.....rr.
.rr......rrrr......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rr.......rr.......rr.
.rrr......rr......rrr.
.rrrr.....rr.....rrrr.
.rr.rr....rr....rr.rr.
.rr..rr...rr...rr..rr.
.rr...rr..rr..rr...rr.
.rr....rrrrrrrr....rr.
.rr...rrrrrrrrrr...rr.
.rr.......rr.......rr.
......................
""".strip('\n')



TYPES = {
    '#': Wall,
    'w': Water,
    't': Tree,
    'r': Road,
    's': Stump,
    'k': Rocks,
    'R': RadientAncient,
    'D': DareAncient,
    'h': HardWall
}


class BigMap(Map):
    @classmethod
    def init(cls, game: Game, repository: PlayersRepository):

        for template, target in ((BACKGROUND, game.backgrounds), (TEMPLATE, game.objects)):

            template = template.replace(' ', '')
            rows = template.split('\n')

            width = len(rows)
            height = len(rows[0])
            game.size = (width, height)

            for i in range(len(rows)):
                for j in range(len(rows[i])):
                    if rows[i][j] in TYPES:
                        target[(i, j)] = TYPES[rows[i][j]]()

        template = TEMPLATE.replace(' ', '')
        rows = template.split('\n')

        for i in range(len(rows)):
            for j in range(len(rows[i])):
                if rows[i][j] == 'T':
                    game.players[(i, j)] = Tower('Radient' if i >= width // 2 else 'Dare')

        for i in range(20):
            while True:
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)

                if (x, y) in game.objects or (x, y) in game.items or (x, y) in game.players:
                    continue

                game.items[(x, y)] = SniperBooster()
                break

        for i in range(20):
            while True:
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)

                if (x, y) in game.objects or (x, y) in game.items or (x, y) in game.players:
                    continue

                game.items[(x, y)] = HealthKit()
                break

            player_descriptions = repository.all()

            for description in player_descriptions:
                for i in range(10):
                    while True:
                        x = random.randint(0, width - 1)
                        y = random.randint(0, height - 1)
                        if (x, y) in game.objects or (x, y) in game.items or (x, y) in game.players:
                            continue
                        game.players[(x, y)] = Player(description[0], repository, {"team": 'Radient' if i < 5 else 'Dare'})
                        break