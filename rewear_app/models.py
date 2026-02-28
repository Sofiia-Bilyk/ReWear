from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

#user model to store user information and their outfits and items
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    password_hash = db.Column(db.String(255), nullable=False)


    outfits = db.relationship('Outfit', backref='user', lazy=True)
    items = db.relationship('Item', backref='user', lazy=True)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

#item model to store information about each clothing item, including its name, category, and the user it belongs to
class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    category = db.Column(db.String(50))
    #ai-detected fields (filled by YOLO pipeline)
    ai_category = db.Column(db.String(80))
    ai_color_primary = db.Column(db.String(50))
    ai_confidence = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    archived_at = db.Column(db.DateTime, nullable=True)  # soft delete

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tags = db.relationship('ItemTag', backref='item', lazy=True)

#customizable labels per item (voted in Feb 21)
class ItemTag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    tag = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

#outfit model to store information about each outfit, including the image path, date worn, and the user it belongs to
class Outfit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String(255), nullable=False)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    worn_date  = db.Column(db.Date, nullable=False, default=datetime.utcnow)  # supports back-dating
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    image_path = db.Column(db.String(255), nullable=True)   # optional, can log without photo
    ai_status  = db.Column(db.String(20), default='pending')  # pending/done/failed
    notes = db.Column(db.Text, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

#outfit item model to create a many-to-many relationship between outfits and items
class OutfitItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    outfit_id = db.Column(db.Integer, db.ForeignKey('outfit.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)

    # bounding box from YOLO (for the ai correction UI)
    bbox_x      = db.Column(db.Float)
    bbox_y      = db.Column(db.Float)
    bbox_w      = db.Column(db.Float)
    bbox_h      = db.Column(db.Float)
    # did the user accept or correct the AI detection?
    user_action = db.Column(db.String(20), default='ai_accepted')  # ai_accepted/user_corrected/user_added

#reminder model to store information about reminders for items that haven't been worn in 30+ days
class Reminder(db.Model):
    id            = db.Column(db.Integer, primary_key=True)
    user_id       = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id       = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    remind_at     = db.Column(db.DateTime, nullable=False)
    snoozed_until = db.Column(db.DateTime, nullable=True)
    is_sent       = db.Column(db.Boolean, default=False)
