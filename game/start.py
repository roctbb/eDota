import json
import time
import redis
from domain.game import Game
from domain.maps.default import DefaultMap

r = redis.Redis()

game = Game(DefaultMap)

while True:
    frame = game.make_step()
    r.publish('edota_frame', json.dumps(frame))
    time.sleep(0.5)
