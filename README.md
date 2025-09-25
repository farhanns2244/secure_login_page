<h1>Flask Login & Registration Portal</h1>
<h3>Overview</h3>

  This is a simple and secure user authentication system built with Flask, Flask-SQLAlchemy, and Flask-Mail. It allows users to:

->Register an account with a username and password

->Login securely with password hashing

->Reset forgotten passwords using OTP sent to email

->Implement a security feature that suspends users for 30 seconds after 3 failed login attempts

The portal is lightweight and can be run locally.
<hr>


<h3>Features</h3>

<h4>1.User Registration</h4>

 ->User can register with a unique username (or email).
 
 ->Passwords are hashed using Werkzeug.security before storing in the database.
 
 
<h4>2.User Login</h4>

 ->Login using registered credentials.

 ->Flash messages indicate success or failure.
 
 
<h4>3.Forgot Password(OTP)</h4>

 ->Users can request a password reset by entering their email
 
 ->A 6-digit OTP is sent to the email via Flask-Mail.
 
 ->After OTP verification, users can reset their password.

 
<h4>4.Dashboard</h4>

 ->A simple dashboard page is accessible only to logged-in users.
 
<hr>


<h3>Technologies Uesd</h3>

 ->Python 3.x
 
 ->Flask-Web framework
 
 ->Flask-SQLAlchemy – Database ORM
 
 ->Flask-Mail – Email/OTP functionality
 
 ->Werkzeug – Password hashing
 
 ->SQLite – Database storage
 
 ->HTML/CSS – Frontend
 
<hr>

<h3>Project Structure</h3>

  flask_simple_auth/
  
├── app.py    

├── templates/          

│   ├── base.html

│   ├── register.html

│   ├── login.html

│   ├── dashboard.html

│   ├── forgot.html

│   ├── verify_otp.html

│   └── reset_password.html

├── static/               

│   └── style.css

└── users.db             

<hr>



 



















 
