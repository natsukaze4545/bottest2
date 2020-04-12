import os
from flask import Flask, render_template, g
from hamlish_jinja import HamlishExtension
from werkzeug import ImmutableDict
from flask_sqlalchemy import SQLAlchemy

class FlaskWithHamlish(Flask):
    jinja_options = ImmutableDict(
        extensions=[HamlishExtension]
    )
app = FlaskWithHamlish(__name__)

db_uri = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)

class Entry(db.Model):
    # テーブル名を定義
    __tablename__ = "mamadb"

    # カラムを定義
    user_id = db.Column(db.String(), nullable=False)
    name = db.Column(db.String(), nullable=False)
    point = db.Column(db.String(), nullable=False)
