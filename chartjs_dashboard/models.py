from chartjs_dashboard import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timeStamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    graphModified = db.Column(db.String(100))
    value = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    def __repr__(self):
        return f"{timeStamp}, {graphModified}, {value}"

