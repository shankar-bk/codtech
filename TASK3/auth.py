from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from models import db, User
from flask_jwt_extended import create_access_token
import hashlib

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        pwd = request.form['password']
        hashed = hashlib.sha256(pwd.encode()).hexdigest()
        if User.query.filter_by(username=username).first():
            flash('Username already taken', 'danger')
            return redirect(url_for('auth.register'))
        db.session.add(User(username=username, password=hashed))
        db.session.commit()
        flash('Registered! Please login.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        pwd = hashlib.sha256(request.form['password'].encode()).hexdigest()
        user = User.query.filter_by(username=username, password=pwd).first()
        if not user:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('auth.login'))
        token = create_access_token(identity=user.id)
        # store token in session or cookie if desired
        flash('Logged in!', 'success')
        return redirect(url_for('product.list_products'))
    return render_template('login.html')
