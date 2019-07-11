import click
import sqlite3

class DB:
    DB_NAME = 'sshfk.db'

    def __init__(self):
        self._conn = sqlite3.connect(self.DB_NAME)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def close(self):
        self._conn.close()

    def init_db(self):
        cursor = self._conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS ssh_connection (id INTEGER PRIMARY KEY AUTOINCREMENT, host TEXT, port TEXT, username TEXT, password TEXT, uname TEXT, CONSTRAINT unique_host UNIQUE(host))")
        self._conn.commit()

    def save_ssh_connection(self, host, port, username, password, uname):
        cursor = self._conn.cursor()
        cursor.execute("INSERT INTO ssh_connection(host, port, username, password, uname) VALUES(?, ?, ?, ?, ?)",
            (host, port, username, password, uname))
        self._conn.commit()

    def exists_connection(self, host):
        cursor = self._conn.cursor()
        cursor.execute("SELECT id FROM ssh_connection WHERE host=?", (host,))
        ssh_connection = cursor.fetchone()
        if ssh_connection is None:
            return False

        return True

@click.command()
def init_db():
    with DB() as db:
        db.init_db()

if __name__ == '__main__':
    init_db()
