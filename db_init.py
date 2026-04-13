# db_init.py
from app import app, db, Product

with app.app_context():
    # Database reset (Dhyan rahe, purana data udd jayega)
    db.drop_all()
    db.create_all()
    
    # 400 Products ka Loop
    bulk_products = []
    for i in range(1, 401):
        brand_name = "Rishab-Gold" if i <= 200 else "Rishab-Drivers"
        new_p = Product(
            name=f"LED Model RG-{i:03d}", # RG-001, RG-002...
            brand=brand_name,
            price=float(450 + (i * 5)), # Alag-alag prices
            stock=i % 20 + 5, # Random stock numbers
            image="default.jpg"
        )
        bulk_products.append(new_p)
    
    db.session.add_all(bulk_products)
    db.session.commit()
    print("Mubarak ho Aman! 400 Products database mein load ho gaye hain.")