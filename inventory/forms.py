from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, FloatField, SelectField, DecimalField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, InputRequired

from inventory.models import User, Product


class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already Exist')

    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already Exist')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password',
                             validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('That email is taken. Please choose a different one.')


class ProductForm(FlaskForm):
    prodcode = StringField('Prod Code', validators=[DataRequired()])
    prodname = StringField('Prod Name', validators=[DataRequired()])
    price = DecimalField('Srp', places=2, validators=[InputRequired()])
    category = SelectField('Category', choices=[('Grocery', 'Grocery'), ('Electrical', 'Electrical'), ('Hardware', 'Hardware'),
                                                ('Refreshment', 'Refreshment')], validators=[DataRequired()])
    qty_onhand = FloatField('Qty on Hand', validators=[DataRequired()])
    reorder = FloatField('Re-order', validators=[DataRequired()])
    uom = SelectField('Units', choices=[('pc', 'piece'), ('bx', 'box'), ('k', 'Kilo')])
    location = SelectField('Location', choices=[('Store', 'Store'), ('Warehouse', 'Warehouse')], validators=[DataRequired()])
    remarks = TextAreaField('Remarks')
    picture = FileField('Update Product Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Add')

    def validate_prodcode(self, prodcode):
        if prodcode.data != Product.prodcode:
            product = Product.query.filter_by(prodcode=prodcode.data).first()
            if product:
                raise ValidationError('Product Code Already Exist!')

    def validate_prodname(self, prodname):
        product = Product.query.filter_by(prodname=prodname.data).first()
        if product:
            raise ValidationError('Product Name already Exist!')


class UpdateProductForm(FlaskForm):
    prodcode = StringField('Prod Code', validators=[DataRequired()])
    prodname = StringField('Prod Name', validators=[DataRequired()])
    price = DecimalField('Srp', places=2, validators=[InputRequired()])
    category = SelectField('Category', choices=[('g', 'Grocery'), ('e', 'Electrical'), ('h', 'Hardware'),
                                                ('r', 'Refreshment')], validators=[DataRequired()])
    qty_onhand = FloatField('Qty on Hand', validators=[DataRequired()])
    reorder = FloatField('Re-order', validators=[DataRequired()])
    uom = SelectField('Units', choices=[('pc', 'piece'), ('bx', 'box'), ('k', 'Kilo')])
    location = SelectField('Location', choices=[('s', 'Store'), ('w', 'Warehouse')], validators=[DataRequired()])
    remarks = TextAreaField('Remarks')
    picture = FileField('Update Product Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    #def __init__(self, *args, **kwargs):
    #    super(UpdateProductForm, self).__init__(*args, **kwargs)
    #    read_only(self.prodcode, self.prodname)






