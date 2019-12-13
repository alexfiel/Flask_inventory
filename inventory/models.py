from datetime import datetime
from inventory import db, login_manager
from flask_login import UserMixin
import flask_whooshalchemy
from whoosh.analysis import StemmingAnalyzer

 

# if during the migrate says table not updated run the following command below.
# python manage.py db stamp head / flask db stamp head
# python manage.py db migrate / flask db migrate
# python manage.py db upgrade / flask db upgrade



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    products = db.relationship('Product', backref='author', lazy=True)
    projects = db.relationship('Project', backref='Proj', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Product(db.Model):
    __tablename__ = 'product'
    __searchable__ =['prodname','prodcode']
    __analyzer__ = StemmingAnalyzer()

    id = db.Column(db.Integer, primary_key=True)
    prodcode = db.Column(db.String(50), unique=True, nullable=False)
    prodname = db.Column(db.String(50), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    uom = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    location = db.Column(db.String(50), nullable=True)
    prod_image = db.Column(db.String(20), nullable=False, default='default_product.png')
    re_order = db.Column(db.Float, nullable=False)
    qty_onhand = db.Column(db.Float, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    remarks = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Products('{self.prodname}', '{self.date_posted}'), '{self.prod_image}'"

  
class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    projectcode = db.Column(db.String(50), unique=True, nullable=False)
    projectname = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(200), nullable=True)
    projectlocation = db.Column(db.String(100), nullable=False)
    project_image = db.Column(db.String(20), nullable=False, default='default_product.png')
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Projects('{self.projectname}','{self.projectcode}')"