import sqlite3


class Sqlite:

    def __init__(self):
        pass

    @staticmethod
    def create_accessibility_db():
        acc = sqlite3.connect("accessibility.db")
        acc.cursor()
        acc.execute("""CREATE TABLE accessibility (
                                   timestamp blob,
                                   wcag2a integer,
                                   wcag2aa integer)
                                   """)
        acc.commit()
        acc.close()


Sqlite().create_accessibility_db()
