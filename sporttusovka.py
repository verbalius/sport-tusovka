from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from base64 import b64encode, b64decode
import requests
import json
import secrets
import os, stat
from re import sub
import ssl
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__,
            static_url_path='', 
            static_folder='static',
            template_folder='templates')

app.config['SECRET_KEY'] = os.environ['FLASK_KEY']
socketio = SocketIO(app)
db = SQLAlchemy(app)

### Models

pax = db.Table('pax',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
    )

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    age = db.Column(db.Integer)
    telegram = db.Column(db.String(64))
    email = db.Column(db.String(64), unique=True, nullable=False)
    photo = db.Column(db.String(64))
    description = db.Column(db.Text, nullable=False)
    events = db.relationship('Event', secondary=pax, backref=db.backref('event', lazy='dynamic'))

    def __init__(self, name, age, telegram, email, photo, description):
        self.name = name
        self.age = age
        self.telegram = telegram 
        self.email = email
        self.photo = photo
        self.description = description

    def __repr__(self):
        return '<User %r>' % self.email
    
    def serialize(self):
        return {
            'id': self.id, 
            'name' : self.name,
            'age' : self.age,
            'telegram' : self.telegram, 
            'email' : self.email,
            'photo' : self.photo,
            'description' : self.description
        }

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.Integer)
    startLat = db.Column(db.Float)
    startLon = db.Column(db.Float)
    finishLat = db.Column(db.Float)
    finishLon = db.Column(db.Float)
    level = db.Column(db.Integer)
    length = db.Column(db.Integer)
    creatorID = db.Column(db.Integer)

    def __init__(self, datetime , startLat, length, startLon, finishLon, finishLat, level, creatorID):
        self.datetime = datetime
        self.startLat = startLat
        self.startLon = startLon
        self.finishLat = finishLat
        self.finishLon = finishLon
        self.level = level
        self.length = length
        self.creatorID = creatorID

    def __repr__(self):
        return '<id {}>'.format(self.id)
    
    def serialize(self):
        return {
            'id': self.id,
            'datetime' : datetime,
            'startLat' : startLat,
            'startLon' : startLon,
            'finishLat' : finishLat,
            'finishLon' : finishLon,
            'level' : level,
            'creatorID' : creatorID
        }

### Models

@app.route('/')
def splash():
    return render_template('splash.html')

@app.route('/app')
def map():
    return render_template('map.html')

@socketio.on('login')
def register(data_from_google):
    data_from_google = json.dumps(data_from_google)
    emit('api_results', processing_results_json)

@app.route('/easter_egg')
def easter_egg():
    return "ну вітаю, маладєц, шо скажеш, круто! умєєш, магьош"

if __name__ == '__main__':
    socketio.run(app)