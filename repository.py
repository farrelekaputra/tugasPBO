import sqlite3
from typing import Mapping


class Repository:
    __DB_URL = "data/database.db"

    def __init__(self):
        pass

    def __make_connection(self):
        self.__connection = sqlite3.connect(self.__DB_URL)
        return self.__connection

    def __rollback_connection(self):
        self.__connection.rollback()

    def __setup(self):
        self.__cursor = self.__make_connection().cursor()

    def __end(self):
        self.__cursor.close()
        self.__connection.commit()
        self.__connection.close()

    def get_all(self):
        self.__setup()
        self.__cursor.execute("SELECT * FROM music")
        result = self.__cursor.fetchall()
        self.__end()
        return result

    def get_by_id(self, music_id):
        self.__setup()
        self.__cursor.execute("SELECT * FROM music WHERE id = ?", (music_id,))
        result = self.__cursor.fetchone()
        self.__end()
        return result

    def create(self, data:Mapping[str, str]):
        self.__setup()
        self.__cursor.execute("INSERT INTO music (name, artist, album, duration) VALUES (?, ?, ?, ?)", data)
        self.__end()

    def delete_all(self):
        self.__setup()
        self.__cursor.execute("DELETE FROM music")
        self.__end()

    def delete_by_name(self, name: str):
        self.__setup()
        self.__cursor.execute("DELETE FROM music WHERE id = ?", (name,))
        self.__end()
