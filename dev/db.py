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

def new_user(pseudo:str, firstname:str, lastname:str, sexe:str, email:str, adress:str, city:str, postalcode:str, phone:str, datebirthday:str, password:str):
    db = get_db()
    cur = db.cursor()
    # insérer la ligne dans la table User
    cur.execute(f"INSERT INTO User VALUES ('{pseudo}','{firstname}','{lastname}','{sexe}','{email}','{adress}','{city}','{postalcode}','{phone}','{datebirthday}','{password}')")
    # sauvegarder les changements
    db.commit()