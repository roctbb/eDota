from dataclasses import dataclass
from enum import Enum


@dataclass
class Point:
    x: int
    y: int


class Direction(str, Enum):
    LEFT = "left"
    UP = "up"
    RIGHT = "right"
    DOWN = "down"
    NO = "no"


class Decision(str, Enum):
    FIRE_UP = "fire_up"
    FIRE_LEFT = "fire_left"
    FIRE_RIGHT = "fire_right"
    FIRE_DOWN = "fire_down"
    GO_UP = "go_up"
    GO_LEFT = "go_left"
    GO_RIGHT = "go_right"
    GO_DOWN = "go_down"
    USE = "use"

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def attacks(cls):
        return (cls.FIRE_UP, cls.FIRE_DOWN, cls.FIRE_LEFT, cls.FIRE_RIGHT)

    @classmethod
    def moves(cls):
        return (cls.GO_UP, cls.GO_DOWN, cls.GO_LEFT, cls.GO_RIGHT)


@dataclass
class Position:
    point: Point
    direction: Direction


class Buster:
    def __init__(self, characteristic, value, ticks):
        self.characteristic = characteristic
        self.ticks_left = ticks
        self.value = value

    def tick(self):
        self.ticks_left -= 1

    def over(self):
        return self.ticks_left <= 0

    def apply(self, object):
        if self.characteristic in object.properties:
            object.properties[self.characteristic] += self.value

    def deapply(self, object):
        if self.characteristic in object.properties:
            object.properties[self.characteristic] -= self.value


class Event:
    def __init__(self, type, params):
        self.type = type
        self.params = params

    def as_dict(self):
        return {
            "type": self.type,
            "params": self.params
        }


class Object:
    def __init__(self):
        self.direction = Direction.NO
        self.properties = {}

    def attack(self, power: int):
        if 'life' in self.properties:
            self.properties['life'] -= power

    def alive(self) -> bool:
        return self.properties.get('life', 0) > 0

    def as_dict(self, point: Point = None):
        description = {
            "direction": self.direction,
            "properties": self.properties,
            "type": self.__class__.__name__,
        }

        if point:
            description["x"] = point.x
            description["y"] = point.y

        return description
