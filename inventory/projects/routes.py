import os
import sys
from flask import Blueprint, render_template, flash, url_for, request, abort, redirect
from inventory import db, app, allowed_file, images
from inventory.models import Project
from inventory.projects.forms import ProjectForm
from flask_login import current_user, login_required
from inventory.projects.utils import save_prod_img
from werkzeug.utils import secure_filename


projects = Blueprint('projects', __name__)


@projects.route('/project/register', methods=['GET', 'POST'])
@login_required
def registerProject():
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(projectcode = form.projectcode.data,
                  projectname = form.projectname.data,
                  description = form.description.data,
                  projectlocation = form.projectlocation.data,
                  Proj = current_user)
        db.session.add(project)
        db.session.commit()
        flash('New Project, {}, created!'.format(project.projectname),'success')
        return redirect(url_for('projects.project'))
    return render_template('registerproject.html', title='New Project',
                            form=form, legend='New Project')

@projects.route('/project')
def project():
    projects = Project.query.all()
    return render_template('project.html', title='Project')

       

        
