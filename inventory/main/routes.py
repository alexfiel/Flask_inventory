from flask import Blueprint, render_template, request
from inventory.models import Product
from flask_login import login_required

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)


@main.route('/about')
def about():
    return render_template('about.html', title='About')


@main.route('/upload', methods=['POST', 'GET'])
@login_required
def upload():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            print(image)
            return redirect(request.url)
    return render_template('upload.html', title='Upload')