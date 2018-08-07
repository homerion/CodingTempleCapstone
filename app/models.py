from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin,db.Model):
    __tablename__='User'
    # columns
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(16),index=True, unique=True)
    email=db.Column(db.String(120),index=True, unique=True)
    password_hash=db.Column(db.String(256))
    date_created=db.Column(db.DateTime,default=datetime.now())

    # relationships:
    entries = db.relationship("Entries",backref='User')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password,salt_length=32)

    def check_password(self,password):
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return 'Username: {}, Email: {}'.format(
        self.username,self.email)

tag_map = db.Table('tag_map',
    db.Column('entry_id', db.Integer, db.ForeignKey('Entries.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('Tags.id'))
    )

class Entries(db.Model):
    __tablename__='Entries'
    # columns
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('User.id'),index=True)
    text=db.Column(db.String)
    date_created=db.Column(db.DateTime,default=datetime.now())

    # relationships
    tags = db.relationship("Tags",secondary=tag_map)

    def __repr__(self):
        return 'Entry: {}, By User: {}'.format(
        self.text,self.user_id)


class Tags(db.Model):
    __tablename__='Tags'
    # columns
    id=db.Column(db.Integer,primary_key=True)
    tag=db.Column(db.String,index=True, unique=True)

    # relationships
    entries = db.relationship("Entries",secondary=tag_map)

    def __repr__(self):
        return '{}'.format(
        self.tag)




@login.user_loader
def load_user(id):
    return User.query.get(int(id))
