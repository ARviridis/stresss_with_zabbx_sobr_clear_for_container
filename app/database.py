import sqlite3

import click
from flask import current_app
from flask.cli import with_appcontext

DBNAME = 'DigiSign.db'
conn = sqlite3.connect(DBNAME)
conn = sqlite3.connect(DBNAME, check_same_thread=False)
cr = conn.cursor()
db = cr
db1 = db

def init_db():
    with current_app.open_resource('app/schema.sql') as f:
        conn.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.cli.add_command(init_db_command)

class db2:
 pass

class device:
    # Opens database connection. ПРОЧЕКАТЬ  НУЖНО ЛИ?
    DBNAME = 'DigiSign.db'
    conn = sqlite3.connect(DBNAME)
    conn = sqlite3.connect(DBNAME, check_same_thread=False)
    cr = conn.cursor()
    db1 = cr
    rr = None  #для фильтрации

def __init__(self, name):
        try:
            self.connect = sqlite3.connect(name)
            self.cursor = self.connect.cursor()
        except sqlite3.Error as e:
            print("Error connecting to database.")