import os
import sys
from flask import Blueprint, render_template, flash, url_for, request, abort, redirect
from inventory import db, app, allowed_file, images
from inventory.models import Product, Project
from inventory.projects.forms import ProjectForm
from flask_login import current_user, login_required
from inventory.products.utils import save_prod_img
from werkzeug.utils import secure_filename


projects = Blueprint('projects', __name__)


@projects.route('/project/register', methods=['GET', 'POST'])
@login_required
def registerProject():
    form = ProjectForm()
    if form.validate_on_submit():
        if form.project_image.data:
            picture_file = save_prod_img(form.project_image.data)
        project = Project(projectcode = form.projectcode.data,
                  projectname = form.projectname.data,
                  description = form.description.data,
                  projectlocation = form.projectlocation,
                  project_image = picture_file,
                  user_id = current_user)
        db.session.add(project)
        db.session.commit()
        flash('New Project, {}, created!'.format(project.projectname),'success')
        return redirect(url_for('project.projects'))
    else:
        flash('Error in creating new project.', 'error')
    return render_template('registerproject.html', title='New Project',
                            form=form, legend='New Project')

@projects.route('/project')
def project():
    projects = Project.query.all()
    return render_template('project.html', title='Project')

       

        
