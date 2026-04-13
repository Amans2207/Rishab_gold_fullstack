# app.py ki top line aisi honi chahiye
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key='aman_studio_secret_2026'
# Database setup (SQLite use kar rahe hain, easy and fast)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///rishab_gold.db'
db = SQLAlchemy(app)

ADMIN_USER = "admin"
ADMIN_PASS = "RishabGold@2026" # Ise baad mein change kar lena

@app.route('/login', methods=['GET', 'POST'])
def login():
    # 1. Pehle check karo ki form submit hua hai ya nahi
    if request.method == 'POST':
        # 2. Form se data nikalo (Ye lines missing ho sakti hain tumhare code mein)
        username = request.form.get('username')
        password = request.form.get('password')

        # 3. AB check karo (Ab 'username' associated ho gaya hai value ke saath)
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "<h1>Invalid Credentials! <a href='/login'>Try Again</a></h1>"

    # 4. Agar Method 'GET' hai (matlab page pehli baar khula hai), toh login page dikhao
    # Info pass karna mat bhulna taaki footer error na aaye
    return render_template('login.html', info=info)
    shop_info = {
        'contact': '919156934911', # Apna 10 digit WhatsApp number yahan dalo
        'address': 'Electrical Phase-1, Mumbai, Maharashtra',
        'email': 'singhaman22435@gmail.com',
        'name': 'RISHAB GOLD'
    }

    
@app.route('/admin')
def admin_dashboard():
    # Yahan check karo, wahi spelling honi chahiye jo upar set ki thi
    if not session.get('logged_in'): 
        return redirect(url_for('login'))
    
    products = Product.query.all()
    return render_template('admin_dashboard.html', products=products)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('login'))

# Product Model for 400+ items
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    brand = db.Column(db.String(50), nullable=False) # Brand 1 or Brand 2
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(100), default='default.jpg')

info = {
    'name': 'RISHAB GOLD LIGHTING',
    'address': 'Electrical Phase-1, Godown No. 12, Mumbai, Maharashtra',
    'contact': '919156934911',
    'email': 'singhaman22435@gmail.com',
    'godown_name': 'Rishab Central Warehouse'
}

@app.route('/')
def home():
    # Shop & Godown Details
    info = {
        'name': 'RISHAB GOLD LIGHTING',
        'address': 'Main Market, Industrial Area, Mumbai, Maharashtra',
        'phone': '+91 9156934911',
        'email': 'singhaman22435@gmail.com'
    }
    return render_template('index.html', info=info)

@app.route('/shop/<brand_name>')
def shop(brand_name):
    search = request.args.get('search')
    if search:
        # Search logic: Product name mein search karega
        products = Product.query.filter(Product.brand == brand_name, Product.name.contains(search)).all()
    else:
        products = Product.query.filter_by(brand=brand_name).all()
    return render_template('brand_page.html', brand=brand_name, products=products)

@app.route('/brand/<brand_name>')
def brand_products(brand_name):
    # Search logic
    query = request.args.get('search')
    if query:
        products = Product.query.filter(Product.brand == brand_name, Product.name.contains(query)).all()
    else:
        products = Product.query.filter_by(brand=brand_name).all()
    
    # Ye hai fix: 'info' variable define karo aur render_template mein pass karo
    shop_info = {
        'contact': '919156934911', # Apna 10 digit WhatsApp number yahan dalo
        'name': 'RISHAB GOLD'
    }
    
    return render_template('brand_products.html', 
                           brand=brand_name, 
                           products=products, 
                           info=shop_info) 




@app.route('/payment_success')
def payment_success():
    payment_id = request.args.get('id')
    # Yahan hum Twilio ya PyWhatKit use kar sakte hain
    # Example: pywhatkit.sendwhatmsg_instantly("+91CustomerNo", "Order Confirmed! ID: " + payment_id)
    return render_template('success.html', payment_id=payment_id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        if Product.query.count() == 0:
            p1 = Product(name='5W Cylinder Gold', brand='Rishab-Gold', price=1200.0, stock=50, image='rose_gold.jpg')
            p2 = Product(name='12W Panel Light', brand='Rishab-Gold', price=850.0, stock=100, image='panel.jpg')
            p3 = Product(name='LED Driver 10A', brand='Rishab-Drivers', price=450.0, stock=20, image='driver.jpg')
            db.session.add_all([p1, p2, p3])
            db.session.commit()
            print("Database initialized with test products!") # Database create karega automatic
    app.run(debug=True)

@app.context_processor
def inject_info():
    return {'info': {'contact': '919156934911', 'name': 'RISHAB GOLD'}}