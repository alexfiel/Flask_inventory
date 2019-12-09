import os
import sys
from flask import Blueprint, render_template, flash, url_for, request, abort, redirect
from inventory import db, app, allowed_file, images
from inventory.models import Product
from inventory.products.forms import ProductForm, UpdateProductForm, SearchProductForm
from flask_login import current_user, login_required
from inventory.products.utils import save_prod_img
from werkzeug.utils import secure_filename


products = Blueprint('products', __name__)


@products.route('/product/register', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            #filename = images.save(request.files['picture'])
            filename = "default.jpg"
            newproduct = Product(prodname=form.prodname.data,
                          prodcode=form.prodcode.data,
                          price=form.price.data,
                          category=form.category.data,
                          qty_onhand=form.qty_onhand.data,
                          uom=form.uom.data,
                          re_order=form.reorder.data,
                          location=form.location.data,
                          remarks=form.remarks.data,
                          picture =filename,
                          author=current_user)
            db.session.add(newproduct)
            db.session.commit()
            flash('New Product, {}, added!'.format(newproduct.prodname), 'success')
            return redirect(url_for('main.home'))
        else:
            flash('ERROR! Product not added.', 'error')
    return render_template('registernewproduct.html', form=form)


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
    return render_template('product.html', title=product.prodname, product=product, prod_image = product.prod_image)


@products.route('/product/result', methods=['GET','POST'])
def searchproduct():
    #search = SearchProductForm(request.form)
    products = Product.query.all()
    return render_template('show.html', products=products)
    
    
@products.route('/product/result')
def search_results(search):
    results = []
    search_string = search.data['search']

    if search.data['search'] == '':
        qry = db.session.query(Product)
        results = qry.all()
    
    if not results:
        flash('No results Found!')
        return redirect('/product/result')
    
    else:
        return render_template('productResult.html', results=results)    

@products.route('/product/<int:prod_id>/update', methods=['GET', 'POST'])
@login_required
def update_product(prod_id):
    product = Product.query.get_or_404(prod_id)
    if product.author != current_user:
        abort(403)
    form = UpdateProductForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_prod_img(form.picture.data)
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
                           prod_image=prod_image, form=form, legend='Update Product')


@products.route('/product/<int:prod_id>/delete', methods=['POST'])
@login_required
def delete_product(prod_id):
    product = Product.query.get_or_404(prod_id)
    if product.author != current_user:
        abort(403)
    db.session.delete(product)
    db.session.commit()
    flash('Product has been deleted', 'success')
    return redirect(url_for('main.home'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('main.home',
                                    filename=filename))
    return render_template('upload.html')
