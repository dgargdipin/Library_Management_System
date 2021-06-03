from datetime import timedelta
from lms.models import Issues
from flask import render_template, request,Blueprint
from flask.globals import session
from flask.helpers import url_for
from flask_login import current_user
core=Blueprint('core',__name__)
print("__name__ is ",__name__)

@core.route('/')
def index():
    session['url']=url_for('core.index')
    fifteendays=timedelta(days=15)
    allIssues=Issues.query.filter_by(returned=False).all()
    return render_template('index.html',allIssues=allIssues,fifteendays=fifteendays)

@core.route('/info')
def info():
    return render_template('info.html')