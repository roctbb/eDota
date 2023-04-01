class PlayerDescription:
    def __init__(self, row: tuple):
        self.id = row[0]
        self.name = row[1]
        self.key = row[2]
        self.state = row[3]
        self.code = row[4]
        self.team = row[5]


class PlayersRepository:
    def __init__(self, connection):
        self.connection = connection

    def all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM players WHERE state = 'ready'")

        return [PlayerDescription(row) for row in cursor.fetchall()]

    def get(self, id):
        cursor = self.connection.cursor()
        cursor.execute('SELECT * FROM players WHERE id = %s', (id,))

        return PlayerDescription(cursor.fetchone())
