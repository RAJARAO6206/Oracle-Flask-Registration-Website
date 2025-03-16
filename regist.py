from flask import Flask, render_template, request
import oracledb
from werkzeug.security import generate_password_hash
from model import db, UserRegistration  # Import the model and database instance

# Initialize Oracle client
oracledb.init_oracle_client(lib_dir=r"C:\oracleinstantclient\instantclient-basic-windows\instantclient_23_5")

# Initialize Flask app
regist = Flask(__name__)
regist.config['SQLALCHEMY_DATABASE_URI'] = 'oracle+oracledb://system:oracle@localhost:1521/xe'
regist.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy app with Flask
db.init_app(regist)

# Create the database tables if they do not exist
with regist.app_context():
    db.create_all()

@regist.route('/')
def home():
    return "Welcome to the Registration Page! Go to /register to sign up."

@regist.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "Passwords do not match! Please try again."

        # Check if the username already exists
        existing_user = UserRegistration.query.filter_by(username=username).first()
        if existing_user:
            return "Username already taken! Please choose another."

        try:
            # Hash the password before storing it
            hashed_password = generate_password_hash(password)
            new_user = UserRegistration(username=username, password=hashed_password, confirm_password=confirm_password)
            db.session.add(new_user)
            db.session.commit()
            return "Registration Successful!"
        except Exception as e:
            db.session.rollback()
            return f"An error occurred: {str(e)}"

    return render_template('registration_form.html')

if __name__ == '__main__':
    regist.run(debug=True, port=5007)
