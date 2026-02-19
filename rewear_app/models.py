from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

#user model to store user information and their outfits and items
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    outfits = db.relationship('Outfit', backref='user', lazy=True)
    items = db.relationship('Item', backref='user', lazy=True)

#item model to store information about each clothing item, including its name, category, and the user it belongs to
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#outfit model to store information about each outfit, including the image path, date worn, and the user it belongs to
class Outfit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    date_worn = db.Column(db.Date, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#outfit item model to create a many-to-many relationship between outfits and items
class OutfitItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    outfit_id = db.Column(db.Integer, db.ForeignKey('outfit.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)