from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import  Migrate


app = Flask(__name__)
app.config['SECRET_KEY'] = 'f62518f03b560013049fe43c83133a1c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:cto154@localhost:3306/inventory'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

from inventory.users.routes import users
from inventory.products.routes import products
from inventory.main.routes import main

app.register_blueprint(users)
app.register_blueprint(products)
app.register_blueprint(main)



