import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource(current_app.config['PATH'] + '/schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    # new_user(pseudo="Baratinus", sexe="homme", email="p.baratinus@gmail.com", datebirthday="09/06/2003", password="azerty")

def gestion_db(function):
    """Décorateur pour éviter la répétiton de code
    """
    def function_decorator(*args):
        db = get_db()
        cur = db.cursor()
        f = function(*args, cursor=cur)
        # sauvegarder les changements
        db.commit()
        cur.close()
        return f
    return function_decorator

@gestion_db
def new_user(user, cursor:sqlite3.Cursor=None):
    cursor.execute(f"INSERT INTO User VALUES ('{user.pseudo}','{user.firstname}','{user.lastname}','{user.sexe}','{user.email}','{user.adress}','{user.city}','{user.postalcode}','{user.phone}','{user.datebirthday}','{user.password}')")

@gestion_db
def is_value_in_column(table:str, column:str, value:str, /, cursor:sqlite3.Cursor=None) -> bool:
    cursor.execute(f"SELECT {column} FROM {table} WHERE {column}='{value}'")
    a = len(cursor.fetchall())
    return(a != 0)
