from flask import Blueprint, request, redirect, url_for, render_template, flash
from models import db, Product

product_bp = Blueprint('product', __name__, template_folder='templates')

@product_bp.route('/products')
def list_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@product_bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        p = Product(
            name=request.form['name'],
            price=float(request.form['price']),
            stock=int(request.form['stock'])
        )
        db.session.add(p)
        db.session.commit()
        flash('Product added!', 'success')
        return redirect(url_for('product.list_products'))
    return render_template('add_product.html')
