import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_uploads import UploadSet, IMAGES, configure_uploads


APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/data_pics/product_img')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['SECRET_KEY'] = 'f62518f03b560013049fe43c83133a1c'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:cto154@localhost:3306/inventory'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_pyfile('sys.cfg')


db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'


# Configure the image uploading via FLask-Uploads
images = UploadSet('images', IMAGES)
configure_uploads(app, images)


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1].lower()in ALLOWED_EXTENSIONS


# register the blueprint 
from inventory.users.routes import users
from inventory.products.routes import products
from inventory.main.routes import main
from inventory.projects.routes import projects

app.register_blueprint(users)
app.register_blueprint(products)
app.register_blueprint(main)
app.register_blueprint(projects)






