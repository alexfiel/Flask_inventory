from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FloatField, SelectField, DecimalField
from wtforms.validators import DataRequired, ValidationError, InputRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired
from inventory.models import Project
from inventory import images


class ProjectForm(FlaskForm):
    projectcode = StringField('Project Code', validators=[DataRequired()])
    projectname = StringField('Project Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators =[DataRequired()])
    projectlocation = StringField('Project Location', validators=[DataRequired()])
    project_image = FileField('Project Image', validators=[FileAllowed(['jpg','png'])])
    submit = SubmitField('Register')

    def validate_projectcode(self, projectcode):
        if projectcode.data != Project.projectcode:
            project = Project.query.filter_by(projectcode=projectcode.data).first()
            if project:
                raise ValidationError('Projectcode Already Exist!')

    def validate_projectname(self, projectname):
        project = Project.query.filter_by(projectname = projectname.data).first()
        if project:
            raise ValidationError('Project Name Already Exist!')