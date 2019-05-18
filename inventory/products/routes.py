from flask import Blueprint, render_template, flash, url_for, request, abort, redirect
from inventory import db
from inventory.models import Product
from inventory.products.forms import ProductForm, UpdateProductForm
from flask_login import current_user, login_required


products = Blueprint('products', __name__)


@products.route('/product/new', methods=['GET', 'POST'])
@login_required
def new_product():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(prodname=form.prodname.data,
                          prodcode=form.prodcode.data,
                          price=form.price.data,
                          category=form.category.data,
                          qty_onhand=form.qty_onhand.data,
                          uom=form.uom.data,
                          re_order=form.reorder.data,
                          location=form.location.data,
                          remarks=form.remarks.data,
                          author=current_user)
        db.session.add(product)
        db.session.commit()

        flash('The product has been successfully saved!', 'success')
        return redirect(url_for('main.home'))
    return render_template('new_product.html', title='New Product',
                           form=form, legend='New Product')


@products.route('/product/<int:prod_id>')
def product(prod_id):
    product = Product.query.get_or_404(prod_id)
    return render_template('product.html', title=product.prodname, product=product)


@products.route('/product/<int:prod_id>/update', methods=['GET', 'POST'])
@login_required
def update_product(prod_id):
    product = Product.query.get_or_404(prod_id)
    if product.author != current_user:
        abort(403)
    form = UpdateProductForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            product.prod_image = picture_file
        product.prodname = form.prodname.data
        product.prodcode = form.prodcode.data
        product.price = form.price.data
        product.category = form.category.data
        product.qty_onhand = form.qty_onhand.data
        product.re_order = form.reorder.data
        product.uom = form.uom.data
        product.location = form.location.data
        product.remarks = form.remarks.data
        db.session.commit()
        flash('Your product has been updated!', 'success')
        return redirect(url_for('products.product', prod_id=prod_id))
    elif request.method == 'GET':
        form.prodcode.data = product.prodcode
        form.prodname.data = product.prodname
        form.price.data = product.price
        form.category.data = product.category
        form.qty_onhand.data = product.qty_onhand
        form.reorder.data = product.re_order
        form.uom.data = product.uom
        form.location.data = product.location
        form.remarks.data = product.remarks
    prod_image = url_for('static', filename='data_pics/' + product.prod_image)
    return render_template('update_product.html', title='Update Product',
                           image_file=prod_image, form=form, legend='Update Product')


@products.route('/product/<int:prod_id>/delete', methods=['POST'])
@login_required
def delete_product(prod_id):
    product = Product.query.get_or_404(prod_id)
    if product.author != current_user:
        abort(403)
    db.session.delete(product)
    db.session.commit()
    flash('Product has been deleted', 'success')
    return redirect(url_for('home'))
