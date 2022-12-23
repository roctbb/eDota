
from domain.common import *
from domain.item import Item


class Coin(Item):
    def __init__(self):
        super().__init__()

        self.properties = {
            "life": 100,
        }