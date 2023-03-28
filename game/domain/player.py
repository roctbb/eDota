import sys
import imp

from domain.repositories.players import PlayersRepository
from domain.general_player import GeneralPlayer
from domain.inventory import *


class Player(GeneralPlayer):
    def __init__(self, id: int, repository: PlayersRepository, properties={}):
        super().__init__()

        self.id = id
        self.repository = repository

        for key in properties:
            self.properties[key] = properties[key]

    def _update_decider(self):
        description = self.repository.get(self.id)
        self.properties['name'] = description[1]
        with open(f'./bots/{self.id}.py', 'w') as file:
            file.write(description[4])
        sys.path.append("./bots/")
        module = __import__(f"{self.id}", fromlist=["make_choice"])
        module = imp.reload(module)
        self.decider = getattr(module, "make_choice")

    def step(self, point, map_state):
#        map_state_player = []
#        for i in map_state:
#            cell = []
#            for j in i:
#                if j['player']:
#                    d = {'type' : 'Player'}
#                    d.update(self.properties)
#                    d.update(Player.items)
#                    cell.append(d)
#                else:
#                    cell.append({})
#                if j['items']:
#                    cell.append({'type' : j['items']['type']})
#                else:
#                    cell.append({})
#                if j['object']:
#                    cell.append({'type' : j['object']['type'],
#                                 'properties': j['object']['properties']})
#                else:
 #                   cell.append({})
 #           map_state_player.append(cell)
#            print(map_state_player)
        for booster in self.boosters[:]:
            booster.tick()
            if booster.over():
                self.boosters.remove(booster)
        self._update_decider()
        return super(Player, self).step(point, map_state)
