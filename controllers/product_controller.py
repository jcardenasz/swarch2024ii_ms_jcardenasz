from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from services.products_service import ProductService

product_blueprint = Blueprint('products', __name__)

@product_blueprint.route('/products', methods=['POST'])
def create_product():
    data = request.form
    name = data.get('name')
    description = data.get('description')

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    ProductService.create_product(name, description)
    return redirect(url_for('products.index'))

@product_blueprint.route('/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = ProductService.get_product_by_id(product_id)

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        if not name:
            return jsonify({'error': 'Name is required'}), 400

        ProductService.update_product(product_id, name, description)
        return redirect(url_for('products.index'))

    return render_template('edit_product.html', product=product)

@product_blueprint.route('/')
def index():
    products = ProductService.get_all_products()
    return render_template('index.html', products=products)
