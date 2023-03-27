import json
import time
import redis
from domain.game import Game
from domain.maps.default import DefaultMap
from domain.maps.big import BigMap
from config import *
import psycopg2

from domain.repositories.players import PlayersRepository

r = redis.Redis()
conn = psycopg2.connect(database=PG_DATABASE, user=PG_LOGIN, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT)

repository = PlayersRepository(conn)

while True:
    game = Game()
    BigMap.init(game, repository)

    for step in range(120):
        frame = game.make_step()
        r.publish('edota_frame', json.dumps(frame))
        time.sleep(0.5)