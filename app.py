from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# File Upload Configuration
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads'))
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# MySQL Configuration from env vars or DATABASE_URL (Railway)
import urllib.parse

db_url = os.getenv('DATABASE_URL')
if db_url and db_url.startswith('mysql://'):
    parsed = urllib.parse.urlparse(db_url)
    MYSQL_USER = urllib.parse.unquote(parsed.username)
    MYSQL_PASSWORD = urllib.parse.unquote(parsed.password)
    MYSQL_HOST = parsed.hostname
    MYSQL_PORT = parsed.port or 3306
    MYSQL_DB = parsed.path[1:]  # remove leading '/'
else:
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DB = os.getenv('MYSQL_DB', 'car_parking')

SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')
app.config['SECRET_KEY'] = SECRET_KEY

# Prod upload folder
UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', '/app/static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def get_db_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=getattr(globals(), 'MYSQL_PORT', 3306),
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DB,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/')
def car():
    return render_template('car.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/service')
def service():
    return render_template('service.html')

@app.route('/aboutus')
def aboutus():
    return render_template('aboutus.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        car_number = request.form['carNumber']
        owner_name = request.form['ownerName']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (car_number, owner_name, password) VALUES (%s, %s, %s)",
                       (car_number, owner_name, hashed_password))
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash('Registration failed. Please try again.', 'error')
        finally:
            cur.close()
            conn.close()
    return render_template('registration.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        car_number = request.form['login-username']
        password = request.form['login-password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE car_number = %s", (car_number,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['car_number'] = user['car_number']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html')

@app.route('/parking-form', methods=['GET', 'POST'])
def parking_form():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        full_name = request.form['fullName']
        mobile = request.form['mobile']
        email = request.form['email']
        car_number = request.form['carNumber']
        checkin_date = request.form['checkinDate']
        checkout_date = request.form['checkoutDate']
        checkin_time = request.form['checkin']
        checkout_time = request.form['checkout']
        parking_plan = request.form['parkingPlan']
        rent_amount = request.form['rent']
        
        # Handle image uploads
        spot_images = []
        if 'images' in request.files:
            files = request.files.getlist('images')
            for file in files:
                if file and file.filename:
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    spot_images.append(filename)
        
        spot_images_str = ','.join(spot_images) if spot_images else None

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("""INSERT INTO parking_bookings 
                       (user_id, full_name, mobile, email, car_number, checkin_date, 
                       checkout_date, checkin_time, checkout_time, parking_plan, rent_amount, spot_images) 
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                       (session['user_id'], full_name, mobile, email, car_number,
                        checkin_date, checkout_date, checkin_time, checkout_time,
                        parking_plan, rent_amount, spot_images_str))
            conn.commit()
            flash('Parking spot booked successfully!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            flash('Booking failed. Please try again.', 'error')
        finally:
            cur.close()
            conn.close()

    return render_template('form.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=False)
