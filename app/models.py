from app import db
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), unique=True, default='NO EMAIL')
    password_hash = db.Column(db.String(128))
    messages = db.relationship('Message', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='reviewer', lazy='dynamic')

    def __init__(self, username, email, pwd):
        self.username = username
        self.email = email
        self.password(pwd)

    def __repr__(self):
        return '<User %r>', self.username

    def password(self, pwd):
        self.password_hash = generate_password_hash(pwd)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Message(db.Model):
    __tablename__ = 'message'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    text = db.Column(db.String(500))
    pub_date = db.Column(db.TIMESTAMP)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='author', lazy='select')

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return '<Message %s>' % self.title


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))
    pub_date = db.Column(db.TIMESTAMP)
    mes_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, mes_id, user_id, text):
        self.mes_id = mes_id
        self.user_id = user_id
        self.text = text
    
    def __repr__(self):
        return '<Comment %s>' % self.text
