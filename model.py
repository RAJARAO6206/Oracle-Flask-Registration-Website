from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy without passing Flask app

class UserRegistration(db.Model):
    __tablename__ = 'registrationsss'  # Specify the table name explicitly

    id = db.Column(db.Integer, primary_key=True)  # Primary key
    username = db.Column(db.String(100), nullable=False, unique=True)  # Unique username
    password = db.Column(db.String(200), nullable=False)  # Hashed password
    confirm_password = db.Column(db.String(200))  # Optional; generally not stored in DB

    def __repr__(self):
        return f'<User {self.username}>'
