import imp
import random
import sys
from domain.items.coin import Coin
from domain.items.sniper import SniperBooster
from domain.map import Map
from domain.game import Game
from domain.common import Position, Point, Direction
from domain.objects.wall import Wall
from domain.player import Player
from domain.repositories.players import PlayersRepository
from domain.units.tower import Tower

TEMPLATE = """
........................
.######################.
.#....................#.
.#.....###....###.....#.
.#.....#...TT...#.....#.
.#.....#........#.....#.
.#.....#........#.....#.
.###.T.##########.T.###.
........................
........................
.#.....#..TTTT..#.....#.
.#.....#........#.....#.
.#.....#........#.....#.
.#.....#........#.....#.
........................
........................
##.###.###.....###.##.##
.#.#.....#.....#....#.#.
........................
.#.#.....#.....#....#.#.
##.###.###.....###.##.##
........................
........................
##.###.###.....###.##.##
.#.#.....#.....#....#.#.
........................
.#.#.....#.....#....#.#.
##.###.###.....###.##.##
........................
........................
.#.....#........#.....#.
.#.....#........#.....#.
.#.....#........#.....#.
.#.....#..TTTT..#.....#.
........................
........................
.###.T.##########.T.###.
.#.....#........#.....#.
.#.....#........#.....#.
.#.....#...TT...#.....#.
.#.....###....###.....#.
.#....................#.
.######################.
........................
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
                if rows[i][j] == 'T':
                    game.players[(i, j)] = Tower()

        for i in range(20):
            while True:
                x = random.randint(0, width - 1)
                y = random.randint(0, height - 1)

                if (x, y) in game.objects or (x, y) in game.items:
                    continue

                game.items[(x, y)] = SniperBooster()
                break

        player_descriptions = repository.all()

        for description in player_descriptions:
            for i in range(10):
                while True:
                    x = random.randint(0, width - 1)
                    y = random.randint(0, height - 1)

                    if (x, y) in game.objects or (x, y) in game.items:
                        continue

                    game.players[(x, y)] = Player(description[0], repository)
                    break
