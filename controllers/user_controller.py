from flask import Blueprint, redirect, render_template, session, url_for
from models.loan import Loan
from datetime import datetime, timedelta

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    loans = Loan.query.filter_by(user_id=session['user_id'], is_returned=False).all()

    for loan in loans:
        loan.due_date = loan.loan_date + timedelta(days=30)
        loan.days_remaining = (loan.due_date - datetime.now()).days
    
    return render_template('user_dashboard.html', loans=loans)
