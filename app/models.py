from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin,db.Model):
    # columns
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(16),index=True, unique=True)
    email=db.Column(db.String(120),index=True, unique=True)
    password_hash=db.Column(db.String(256))

    # relationships:
    entries = db.relationship("Entries",backref='user')
    # tags = db.relationship("Tags_Map", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return 'Username: {}, Email: {}'.format(
        self.username,self.email)

class Entries(db.Model):
    # columns
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    text=db.Column(db.String)

    # relationships
    tag = db.relationship("Tag_Map",backref="Entries")

    def __repr__(self):
        return 'Entry: {}, By: {}'.format(
        self.text,self.user_id)

class Tags(db.Model):
    # columns
    id=db.Column(db.Integer,primary_key=True)
    tag=db.Column(db.String, unique=True)

    # relationships
    entry = db.relationship("Tag_Map",backref="Tags")

    def __repr__(self):
        return '{}'.format(
        self.tag)

class Tag_Map(db.Model):
    # columns
    id=db.Column(db.Integer,primary_key=True)
    entry_id=db.Column(db.Integer,db.ForeignKey('entries.id'))
    tag_id=db.Column(db.Integer,db.ForeignKey('tags.id'))

    # relationships
    # user = db.relationship("Tags_Map", backref=db.backref("role", lazy="joined"))
    # entry = db.relationship("Tags_Map", backref=db.backref("role", lazy="joined"))
    # tag = db.relationship("Tags_Map", backref=db.backref("role", lazy="joined"))


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
