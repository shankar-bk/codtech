from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import db, Order, Product
from flask_jwt_extended import jwt_required, get_jwt_identity

order_bp = Blueprint('order', __name__, template_folder='templates')

@order_bp.route('/orders')
@jwt_required()
def view_orders():
    user_id = get_jwt_identity()
    orders = Order.query.filter_by(user_id=user_id).all()
    return render_template('orders.html', orders=orders)

@order_bp.route('/orders/place', methods=['GET', 'POST'])
@jwt_required()
def place_order():
    if request.method == 'POST':
        user_id = get_jwt_identity()
        product_id = int(request.form['product_id'])
        qty = int(request.form['quantity'])
        # optional: check stock
        db.session.add(Order(user_id=user_id, product_id=product_id, quantity=qty))
        db.session.commit()
        flash('Order placed!', 'success')
        return redirect(url_for('order.view_orders'))
    products = Product.query.all()
    return render_template('place_order.html', products=products)
