import sqlite3


class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS game_history
                               (player text, position_from text, position_to text)''')

    def insert_move(self, player, position_from, position_to):
        self.cursor.execute(
            'INSERT INTO game_history VALUES (?, ?, ?)', (player, position_from, position_to))
        self.conn.commit()

    def close(self):
        self.conn.close()
