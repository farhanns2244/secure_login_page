from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

from flask_mail import Mail, Message
import random, smtplib
import requests




app = Flask(__name__)
app.secret_key = "supersecret"  # change in real projects

# Database setup (SQLite file)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    is_verified = db.Column(db.Boolean, default=False)
    otp = db.Column(db.String(6))

# Flask-Mail configuration (use Gmail )
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'farhanns2244@gmail.com'  # your email
app.config['MAIL_PASSWORD'] = 'uvkc htog byne hxxn'    # Gmail app password, not normal password
app.config['MAIL_DEFAULT_SENDER'] = 'youremail@gmail.com'

mail = Mail(app)

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        recaptcha_response = request.form.get('g-recaptcha-response')
        secret_key = '6LeEz9MrAAAAANYr35CtH0mPNzPxyL4_xwLM54T6'

        # Verify CAPTCHA
        payload = {'secret': secret_key, 'response': recaptcha_response}
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
        result = r.json()

        if not result.get('success'):
            flash("CAPTCHA verification failed. Please try again.", "danger")
            return redirect(url_for('register'))

        # Check if username exists
        existing = User.query.filter_by(username=username).first()
        if existing:
            flash("Username already exists!", "danger")
            return redirect(url_for('register'))

        #check if email exists
        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("You already have an account on this email id!", "danger")
            return redirect(url_for('register'))


        # Hash password and create user
        hashed_pw = generate_password_hash(password)

        #generate otp(6 digit)
        otp=str(random.randint(100000, 999999))

        new_user = User(username=username, password=hashed_pw, email=email)
        db.session.add(new_user)
        db.session.commit()

        #send otp to user email
        send_otp_email(email, otp)

        flash("OTP has been sent to your email.", "info")
        return redirect(url_for('verify_otp', username=new_user.username))

    return render_template('register.html')

def send_otp_email(to_email, otp):
    import smtplib
    from email.mime.text import MIMEText

    sender_email = "farhanns2244@gmail.com"
    app_password = "uvkc htog byne hxxn"   # from Google App Passwords

    msg = MIMEText(f"Your OTP is: {otp}")
    msg['Subject'] = "Email Verification OTP"
    msg['From'] = sender_email
    msg['To'] = to_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(sender_email, app_password)
    server.send_message(msg)
    server.quit()

@app.route('/verify_otp/<username>', methods=['GET', 'POST'])
def verify_otp(username):
    user = User.query.filter_by(username=username).first()
    if request.method == 'POST':
        entered_otp = request.form['otp']
        if user and str(user.otp) == entered_otp:
            user.is_verified = True
            user.otp = None   # clear OTP after use
            db.session.commit()
            flash("Your email is verified! Please login.", "success")
            return redirect(url_for('login'))
        else:
            flash("Invalid OTP, try again.", "danger")
    return render_template('verify_otp.html', username=username)

@app.route('/resend_otp/<username>', methods=['POST'])
def resend_otp(username):
    user = User.query.filter_by(username=username).first()
    if user:
        # Generate new OTP
        new_otp = str(random.randint(100000, 999999))
        user.otp = new_otp
        db.session.commit()

        # Send OTP via email again
        send_otp_email(user.email, new_otp)

        flash("A new OTP has been sent to your email.", "info")
    else:
        flash("User not found.", "danger")

    return redirect(url_for('verify_otp', username=username))


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("Logged in successfully!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials!", "danger")
    return render_template('login.html')

#forget
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()

        if user:
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            db.session.commit()

            send_otp_email(user.email, otp)
            flash("An OTP has been sent to your email.", "info")
            return redirect(url_for('forgot_verify_otp', username=user.username))
        else:
            flash("Email not found!", "danger")
            return redirect(url_for('forgot_password'))

    return render_template('forgot_password.html')

@app.route('/forgot_verify_otp/<username>', methods=['GET', 'POST'])
def forgot_verify_otp(username):
    user = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        entered_otp = request.form['otp']
        if user and user.otp == entered_otp:
            user.otp = None
            db.session.commit()
            flash("OTP verified! Please reset your password.", "success")
            return redirect(url_for('reset_password', username=username))
        else:
            flash("Invalid OTP!", "danger")

    return render_template('forgot_verify_otp.html', username=username)

@app.route('/reset_password/<username>', methods=['GET', 'POST'])
def reset_password(username):
    user = User.query.filter_by(username=username).first()

    if request.method == 'POST':
        new_password = request.form['password']
        hashed_pw = generate_password_hash(new_password)
        user.password = hashed_pw
        db.session.commit()

        flash("Password reset successful! You can now login.", "success")
        return redirect(url_for('login'))

    return render_template('reset_password.html', username=username)

# Dashboard (only logged in users)
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash("Please log in first!", "warning")
        return redirect(url_for('login'))
    return render_template('dashboard.html')

# Logout
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash("Logged out successfully!", "info")
    return redirect(url_for('home'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
