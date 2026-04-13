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

    class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=False)
    items = db.Column(db.Text, nullable=False) # JSON string mein products save karenge
    total_amount = db.Column(db.Float, nullable=False)
    payment_id = db.Column(db.String(100), unique=True)
    status = db.Column(db.String(20), default='Paid') 
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)