from domain.general_player import GeneralPlayer


def tower_choice(x, y, state):
    me = state[x][y]['player']
    distance = me['properties']['fire_distance']

    for i in range(x - 1, x - distance, -1):
        if state[i][y]['player'] and state[i][y]['player']['type'] == 'Player':
            return "fire_left"
    for i in range(x + 1, x + distance):
        if state[i][y]['player'] and state[i][y]['player']['type'] == 'Player':
            return "fire_right"
    for i in range(y - 1, y - distance, -1):
        if state[x][i]['player'] and state[x][i]['player']['type'] == 'Player':
            return "fire_up"
    for i in range(y + 1, y + distance):
        if state[x][i]['player'] and state[x][i]['player']['type'] == 'Player':
            return "fire_down"


class Tower(GeneralPlayer):
    def __init__(self, team='Neutral'):
        super().__init__()

        self.decider = tower_choice

        self.properties = {
            'speed': 0,
            'power': 3,
            'life': 10,
            'fire_distance': 4,
            'name': 'tower',
            'team': team
        }

