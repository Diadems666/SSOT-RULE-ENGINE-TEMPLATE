from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.urls import url_parse
from bottle_shop import db
from bottle_shop.models import User
from werkzeug.security import generate_password_hash

# Create auth blueprint
auth_bp = Blueprint('auth', __name__)

# Flag to track if admin user has been created
_admin_created = False

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login"""
    # If user is already logged in, redirect to index
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    # Simple login functionality - would normally use WTForms
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validate input
        if not username or not password:
            flash('Please enter username and password', 'danger')
            return render_template('auth/login.html')
        
        # Find user by username
        user = db.session.execute(
            db.select(User).where(User.username == username)
        ).scalar_one_or_none()
        
        # Check if user exists and password is correct
        if user is None or not user.check_password(password):
            flash('Invalid username or password', 'danger')
            return render_template('auth/login.html')
        
        # Login user
        login_user(user, remember=request.form.get('remember') == 'on')
        
        # Redirect to requested page or home
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        
        return redirect(next_page)
    
    # GET request - display login form
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Handle user logout"""
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('main.index'))

# Create admin user if none exists
@auth_bp.before_app_request
def create_admin_user():
    """Create admin user if none exists (on first request only)"""
    global _admin_created
    if not _admin_created:
        _admin_created = True
        try:
            # Check if admin user already exists
            admin = db.session.execute(
                db.select(User).where(User.username == 'admin')
            ).scalar_one_or_none()
            
            if admin is None:
                admin = User(username='admin', email='admin@example.com', is_admin=True)
                admin.set_password('admin')  # In production, use a secure password
                db.session.add(admin)
                db.session.commit()
                current_app.logger.info('Admin user created successfully')
        except Exception as e:
            current_app.logger.error(f"Error creating admin user: {e}") 