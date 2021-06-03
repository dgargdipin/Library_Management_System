from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager
from flask_migrate import Migrate

app =Flask(__name__,static_url_path='/static/')
app.config['SECRET_KEY']='mysecret'
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, '..', '..', 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)
migrate = Migrate(app, db,
render_as_batch=True)

login_manager=LoginManager()
login_manager.init_app(app)
# login_manager.login_view = 'users.login'
import lms.models
# import cms.branch_helper as branch_helper

db.create_all()
# db.session.add_all(branch_helper.create_branch_array())
# db.session.commit()
from lms.core.views import core
from lms.books.views import books
# from cms.error_pages.handlers import error_pages
from lms.auth.views import auth
from lms.friends.views import friends
# from cms.course.views import CourseBluerint
app.register_blueprint(auth)
app.register_blueprint(core)
app.register_blueprint(books)
app.register_blueprint(friends)
# app.register_blueprint(error_pages)
# app.register_blueprint(CourseBluerint)
# print("route path is, ", core.root_path )

