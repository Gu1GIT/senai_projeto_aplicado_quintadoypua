"""Defines database connection"""

import sqlite3
import click
from flask import Flask, current_app, g

def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return {key: value for key, value in zip(fields, row)}

def get_db():
    """Return database connection if exists or create a new one"""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = dict_factory

    return g.db

def close_db(e=None):
    """Close the database connection"""
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """initialize database and execute sql schema file"""
    db = get_db()

    with current_app.open_resource('./data/database/schema.sql') as f:
        db.executescript(f.read().decode())

def seed_db():
    db = get_db()

    with current_app.open_resource('./data/database/seed.sql') as f:
        db.executescript(f.read().decode())

@click.command('init-db')
def init_db_command():
    """execute init_db function"""
    init_db()
    click.echo('Initialized the database...')

@click.command('seed-db')
def seed_db_command():
    """execute init_db function"""
    seed_db()
    click.echo('Database filled with some data...')


def init_app(app: Flask):
    """set close_db to be called after return any response and register init_db_command to cli"""
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(seed_db_command)
