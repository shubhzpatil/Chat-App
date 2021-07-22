from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    usernm = db.Column(db.String(25), unique=True)
    passw = db.Column(db.String())
