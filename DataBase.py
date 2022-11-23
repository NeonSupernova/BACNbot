import sqlite3
import os

from ApexApi import ApexApi
from MLBBApi import MLBBApi


class DataBase:
    def __init__(self, server_id):
        self.db = f"./dbs/{server_id}.db"
        if not os.access("./dbs", os.F_OK):
            os.mkdir("./dbs")
        if not os.access(self.db, os.F_OK):
            self.con = sqlite3.connect(self.db)
            self.cur = self.con.cursor()
        else:
            self.con = sqlite3.connect(self.db)
            self.cur = self.con.cursor()

    async def add_to_mlbb_db(self, discord_id, user_id: int, zone_id: int):
        mlbb = MLBBApi(user_id, zone_id)
        if mlbb.username is '':
            return 'Bad User ID or Zone ID'
        else:
            CREDS = (discord_id, int(user_id), int(zone_id))
            for row in self.cur.execute('SELECT * FROM MLBB_REGISTRY'):
                if row == CREDS:
                    return 'Already registered'
            self.cur.execute('INSERT INTO MLBB_REGISTRY VALUES (?, ?, ?)', CREDS)
            self.con.commit()
            return 'Successfully Added'

    async def add_to_apex_db(self, discord_id, player_id: int, platform):
        apex = ApexApi(player_id, platform)

    async def disconnect(self):
        self.con.commit()
        self.con.close()