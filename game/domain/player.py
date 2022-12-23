from domain.common import Object, Position, Decision, Point, Direction
from domain.inventory import Inventory
from typing import Tuple, Callable, Optional
from uuid import uuid4

from domain.item import Item


class Player(Object):
    def __init__(self, properties: dict, decider: Callable, startpack: Tuple[Item]):
        super().__init__()
        self.direction = Direction.LEFT
        self.inventory = Inventory(startpack)
        self.properties = {
            'speed': 1,
            'power': 1,
            'life': 10
        }
        for key in properties:
            self.properties[key] = properties[key]
        self.decider = decider
        self.history = []
        self.errors = []
        self.id = uuid4()
        self.busters = []

    def as_dict(self, point):
        base = super().as_dict(point)
        base['errors'] = [str(e) for e in self.errors]
        base['history'] = self.history
        return base

    def step(self, point: Point, map_state) -> Optional[Decision]:
        try:
            choice = self.decider(point.x, point.y, map_state)
        except Exception as e:
            self.errors.append(e)
            self.history.append("crash")
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
