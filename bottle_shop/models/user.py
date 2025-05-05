from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from bottle_shop import db

class User(db.Model, UserMixin):
    """
    User model for authentication.
    
    This model represents a user who can log into the application.
    It includes fields for username, email, and password.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        """Set password hash from raw password"""
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        """Check if raw password matches stored hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        """String representation of the user"""
        return f'<User {self.username}>' 