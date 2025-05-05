from flask import Blueprint, render_template, redirect, url_for
from datetime import date

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Home page route - redirects to today's takings page."""
    today = date.today()
    return redirect(url_for('takings.view_date', year=today.year, month=today.month, day=today.day))

@main_bp.route('/about')
def about():
    """About page with information about the application."""
    return render_template('about.html') 