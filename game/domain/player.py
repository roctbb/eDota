import traceback

from domain.common import Object, Position, Decision, Point, Direction
from domain.inventory import Inventory
from typing import Tuple, Callable, Optional
from uuid import uuid4
import sys
import imp
from domain.item import Item
from domain.repositories.players import PlayersRepository


class Player(Object):
    def __init__(self, id: int, repository: PlayersRepository):
        super().__init__()
        self.id = id
        self.repository = repository
        self.direction = Direction.LEFT
        self.inventory = Inventory()
        self.properties = {
            'speed': 1,
            'power': 1,
            'life': 10
        }

        self.history = []
        self.errors = []
        self.busters = []

    def as_dict(self, point):
        base = super().as_dict(point)
        base['errors'] = [str(e) for e in self.errors]
        base['history'] = self.history
        return base

    def _update_decider(self):
        description = self.repository.get(self.id)
        self.properties['name'] = description[1]
        with open(f'./bots/{self.id}.py', 'w') as file:
            file.write(description[4])
        sys.path.append("./bots/")
        module = __import__(f"{self.id}", fromlist=["make_choice"])
        module = imp.reload(module)
        self.decider = getattr(module, "make_choice")

    def step(self, point: Point, map_state) -> Optional[Decision]:
        try:
            self._update_decider()
            choice = self.decider(point.x, point.y, map_state)
        except Exception as e:
            self.errors.append(e)
            self.history.append("crash")
            print(traceback.format_exc(), e)
            return

        parts = choice.split()

        if not Decision.has_value(parts[0]):
            self.errors.append(Exception("Invalid choice: " + choice))
            self.history.append("invalid_choice")
            return
        else:
            self.history.append(choice)

        if parts[0] == Decision.USE:
            if len(parts) != 2:
                self.errors.append(Exception("Invalid choice: " + choice))
                self.history.append("invalid_choice")
                return

            item = self.inventory.pop(parts[1])
            if not item:
                self.errors.append(Exception("No item in inventory: " + choice))
                self.history.append("invalid_choice")
                return

            item.apply(self)
            return None
        else:
            return parts[0]

    def rotate(self, direction: Direction):
        self.direction = direction
