from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FloatField, SelectField, DecimalField
from wtforms.validators import DataRequired, ValidationError, InputRequired
from flask_wtf.file import FileField, FileAllowed
from inventory.models import Product

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
    category = SelectField('Category', choices=[('Grocery', 'Grocery'), ('Electrical', 'Electrical'), ('Hardware', 'Hardware'),
                                                ('Refreshment', 'Refreshment')], validators=[DataRequired()])
    qty_onhand = FloatField('Qty on Hand', validators=[DataRequired()])
    reorder = FloatField('Re-order', validators=[DataRequired()])
    uom = SelectField('Units', choices=[('pc', 'piece'), ('bx', 'box'), ('k', 'Kilo')])
    location = SelectField('Location', choices=[('Store', 'Store'), ('Warehouse', 'Warehouse')], validators=[DataRequired()])
    remarks = TextAreaField('Remarks')
    picture = FileField('Update Product Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    #def __init__(self, *args, **kwargs):
    #    super(UpdateProductForm, self).__init__(*args, **kwargs)
    #    read_only(self.prodcode, self.prodname)
