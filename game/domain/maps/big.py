import imp
import random
import sys
from domain.items.coin import Coin
from domain.items.healthkit import HealthKit
from domain.items.sniper import SniperBooster
from domain.map import Map
from domain.game import Game
from domain.common import Position, Point, Direction
from domain.objects.ancients import RadientAncient, DareAncient
from domain.objects.road import Road
from domain.objects.rocks import Rocks
from domain.objects.stump import Stump
from domain.objects.tree import Tree
from domain.objects.wall import Wall
from domain.objects.water import Water
from domain.player import Player
from domain.repositories.players import PlayersRepository
from domain.units.tower import Tower

TEMPLATE = """
....................
..tttttttttttttttt..
..tt............tt..
..t..##########..t..
.....#........#.....
..t..T...DD...T..t..
..s..T...DD...T..t..
..t..T...rr...T..s..
..t..#...rr...#..t..
..t..####TT####..t..
..tt.....rr.....tt..
..ttt.sttrrttt.ktt..
.........rr.........
.#.ttttt.rr.ttttt.#.
.#.t...t.rr.t...t.#.
.#.t.t.t.rr.t.t.t.#.
.#...t.t.rr.t.t...#.
##tttt...rr...tttt##
.........rr.....k...
.....TT..rr....k.k..
ttt..rrrrrr...k.k...
..t..rrrrrr......k..
.....rr.......k.k...
..t..rr........k....
ttt..rr..wwwwwwwwwsw
ttt..rr..wwwwwwwwwsw
..t..rr..ww.........
.....rr..ww..TT.....
..t..rrrrrrrrrr..ttt
ttt..rrrrrrrrrr..t..
.....TT..ww..rr.....
.........ww..rr..t..
wswwwwwwwww..rr..ttt
wswwwwwwwww..rr..ttt
...k.........rr..t..
.k...k.......rr.....
....k....rrrrrr..t..
..k......rrrrrr..ttt
...k.k...rr..TT.....
....k....rr.........
##tttt...rr...tttt##
.#...t.t.rr.t.t...#.
.#.t.t.t.rr.t.t.t.#.
.#.t...t.rr.t...t.#.
.#.ttttt.rr.ttttt.#.
.........rr.........
..ttt.sttrrttt.rtt..
..tt.....rr.....tt..
..t..####TT####..t..
.....#...rr...#.....
..t..T...rr...T..t..
..s..T...RR...T..t..
..t..T...RR...T..s..
..t..#........#..t..
..t..##########..t..
..tt............tt..
..tttttttttttttttt..
....................
""".strip('\n')


class BigMap(Map):
    @classmethod
    def init(cls, game: Game, repository: PlayersRepository):
        template = TEMPLATE.replace(' ', '')
        rows = template.split('\n')

        width = len(rows)
        height = len(rows[0])
        game.size = (width, height)

        for i in range(len(rows)):
            for j in range(len(rows[i])):
                if rows[i][j] == '#':
                    game.objects[(i, j)] = Wall()
                if rows[i][j] == 'w':
                    game.objects[(i, j)] = Water()
                if rows[i][j] == 'T':
                    game.players[(i, j)] = Tower()
                if rows[i][j] == 't':
                    game.objects[(i, j)] = Tree()
                    game.objects[(i, j)].direction = random.choice(Direction.directions())
                if rows[i][j] == 'r':
                    game.objects[(i, j)] = Road()
                if rows[i][j] == 's':
                    game.objects[(i, j)] = Stump()
                if rows[i][j] == 'k':
                    game.objects[(i, j)] = Rocks()
                if rows[i][j] == 'R':
                    game.objects[(i, j)] = RadientAncient()
                if rows[i][j] == 'D':
                    game.objects[(i, j)] = DareAncient()


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

                    game.players[(x, y)] = Player(description[0], repository)
                    break
