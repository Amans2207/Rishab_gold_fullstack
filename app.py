from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
import razorpay

app = Flask(__name__)
app.secret_key = 'aman_studio_secret_2026'

# Database setup
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rishab_gold.db'
db = SQLAlchemy(app)

# Razorpay Setup (Aman, Secret Key yahan replace kar dena)
RAZORPAY_KEY_ID = 'rzp_test_SczZ2gzM8SNac2'
RAZORPAY_KEY_SECRET = 'mHXPZRlLeBmFYUyieeuP5EVv' 
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

ADMIN_USER = "admin"
ADMIN_PASS = "RishabGold@2026"

# --- DATABASE MODELS ---

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), default='default.jpg')

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    total_amount = db.Column(db.Float)
    payment_id = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Pending')

# --- CONTEXT PROCESSOR (For Footer/Navbar Info) ---

@app.context_processor
def inject_info():
    shop_info = {
        'contact': '919156934911',
        'address': 'Electrical Phase-1, Mumbai, Maharashtra',
        'email': 'singhaman22435@gmail.com',
        'name': 'RISHAB GOLD'
    }
    return dict(info=shop_info)

# --- ROUTES ---

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid Credentials!", "danger")
    return render_template('login.html')

@app.route('/admin')
def admin_dashboard():
    if not session.get('logged_in'): 
        return redirect(url_for('login'))
    products = Product.query.all()
    return render_template('admin_dashboard.html', products=products)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/brand/<brand_name>')
def brand_products(brand_name):
    search = request.args.get('search')
    if search:
        products = Product.query.filter(Product.brand == brand_name, Product.name.contains(search)).all()
    else:
        products = Product.query.filter_by(brand=brand_name).all()
    return render_template('brand_products.html', products=products, brand=brand_name)

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    cart = session['cart']
    product = Product.query.get(product_id)
    
    if product:
        cart.append({
            'id': product.id,
            'name': product.name,
            'price': product.price,
            'image': product.image
        })
        session['cart'] = cart
        session.modified = True
        flash(f"{product.name} added to cart!", "success")
    return redirect(request.referrer or url_for('home'))

@app.route('/cart')
def view_cart():
    items = session.get('cart', [])
    total = sum(item['price'] for item in items)
    return render_template('cart.html', items=items, total=total)

@app.route('/remove_from_cart/<int:index>')
def remove_from_cart(index):
    if 'cart' in session:
        cart = session['cart']
        if 0 <= index < len(cart):
            cart.pop(index)
            session['cart'] = cart
            session.modified = True
    return redirect(url_for('view_cart'))

@app.route('/clear_cart')
def clear_cart():
    session.pop('cart', None) # Cart ko session se delete karega
    session.modified = True
    flash("Cart has been cleared!", "info")
    return redirect(url_for('view_cart'))

@app.route('/checkout')
def checkout():
    items = session.get('cart', [])
    if not items:
        flash("Cart is empty!", "warning")
        return redirect(url_for('home'))

    total_amount = sum(item['price'] for item in items)
    
    # Razorpay Order Creation
    data = {
        "amount": int(total_amount * 100), 
        "currency": "INR", 
        "payment_capture": 1 
    }
    order = client.order.create(data=data)
    
    return render_template('checkout.html', 
                           items=items, 
                           total=total_amount, 
                           amount=order['amount'], 
                           order_id=order['id'], 
                           key_id=RAZORPAY_KEY_ID)

@app.route('/payment_success', methods=['POST', 'GET'])
def payment_success():
    # Success ke baad data save karo
    pay_id = request.args.get('pay_id') or request.form.get('razorpay_payment_id')
    name = request.args.get('name') or request.form.get('name')
    
    # Order database mein save karna (Optional but recommended)
    # new_order = Order(customer_name=name, payment_id=pay_id, status='Paid')
    # db.session.add(new_order)
    # db.session.commit()

    session.pop('cart', None) # Cart clear
    return render_template('success.html', name=name, pay_id=pay_id)

# 1. Product Delete karne ke liye
@app.route('/delete_product/<int:id>')
def delete_product(id):
    if not session.get('logged_in'): return redirect(url_for('login'))
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
        flash("Product deleted successfully!", "danger")
    return redirect(url_for('admin_dashboard'))

# 2. Naya Product Add karne ke liye
@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    if not session.get('logged_in'): return redirect(url_for('login'))
    if request.method == 'POST':
        name = request.form.get('name')
        brand = request.form.get('brand')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        image = request.form.get('image') # Abhi simple text input le lo image ke liye
        
        new_p = Product(name=name, brand=brand, price=price, stock=stock, image=image)
        db.session.add(new_p)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return render_template('add_product.html') # Ye file tumhe banani padegi

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Test Products add karna
        if Product.query.count() == 0:
            p1 = Product(name='5W Cylinder Gold', brand='Rishab-Gold', price=1200.0, stock=50, image='rose_gold.jpg')
            p2 = Product(name='12W Panel Light', brand='Rishab-Gold', price=850.0, stock=100, image='panel.jpg')
            p3 = Product(name='LED Driver 10A', brand='Rishab-Drivers', price=450.0, stock=20, image='driver.jpg')
            db.session.add_all([p1, p2, p3])
            db.session.commit()
            print("Database initialized!")
    app.run(debug=True)