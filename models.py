from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False) # Rishab Gold ya Other
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    description = db.Column(db.Text)