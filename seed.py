# seed.py
from app import app, db, Product

with app.app_context():
    # Saara purana data saaf karo
    db.drop_all()
    db.create_all()
    
    # Yahan tum apne 400 products ki list bana sakte ho
    products_to_add = [
        Product(name=f'Rishab LED Model {i}', brand='Rishab-Gold', price=500+i, stock=10, image='default.jpg')
        for i in range(1, 401)
    ]
    
    db.session.add_all(products_to_add)
    db.session.commit()
    print("400 Products Successfully Added!")