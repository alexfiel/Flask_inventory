import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, request, abort
from inventory.forms import RegistrationForm, LoginForm, UpdateAccountForm, ProductForm, UpdateProductForm
from inventory import app, db, bcrypt
from inventory.models import User, Product
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route('/home')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)


@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user. is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email= form.email.data, password= hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to login', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user. is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Failed. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/data_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='data_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@app.route('/product/new', methods=['GET', 'POST'])
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
        return redirect(url_for('home'))
    return render_template('new_product.html', title='New Product',
                           form=form, legend='New Product')


@app.route('/product/<int:prod_id>')
def product(prod_id):
    product = Product.query.get_or_404(prod_id)
    return render_template('product.html', title=product.prodname, product=product)


@app.route('/product/<int:prod_id>/update', methods=['GET', 'POST'])
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
        return redirect(url_for('product', prod_id=prod_id))
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


@app.route('/product/<int:prod_id>/delete', methods=['POST'])
@login_required
def delete_product(prod_id):
    product = Product.query.get_or_404(prod_id)
    if product.author != current_user:
        abort(403)
    db.session.delete(product)
    db.session.commit()
    flash('Product has been deleted', 'success')
    return redirect(url_for('home'))


@app.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            print(image)
            return redirect(request.url)
    return render_template('upload.html', title='Upload')



