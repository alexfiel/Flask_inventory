from flask import Blueprint, render_template, request
from inventory.models import Product
from flask_login import login_required
from inventory import app

main = Blueprint('main', __name__)


@main.route('/')
@main.route('/home')
def home():
    products = Product.query.all()
    return render_template('home.html', products=products)






