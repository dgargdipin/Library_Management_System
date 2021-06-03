
import string
#login user
# register user
#logout user
# account update UserForm)
import random
import os
from flask import render_template,url_for,flash,redirect,request,Blueprint,abort
from flask_login import login_user,current_user,logout_user,login_required
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from lms import db,basedir
from lms.models import User
from lms.auth.forms import RegistrationForm,LoginForm,UpdateUserForm
auth=Blueprint('auth',__name__)



@auth.route('/register',methods=['GET', 'POST'])
def register():
    form=RegistrationForm()
    if form.validate_on_submit():
        # user_data={k:v.data for k,v in form}
        # print(user_data)
        if not User.query.filter_by(email=form.email.data).first():
            user=User(name=form.name.data,about=form.about.data,email=form.email.data,password=generate_password_hash(form.password.data))
            db.session.add(user)
            db.session.commit()
            flash('Thanks for registration!',"primary")
            return redirect(url_for('auth.login'))
        else:
            flash("User with email already exists.","warning")
            return redirect(url_for("auth.register"))
    return render_template('register.html',form=form)

@auth.route('/login',methods=['GET', 'POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user =User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user)
            flash('Login success')
            next=request.args.get('next')
            if next==None or not next[0]=='/':
                next=url_for('core.index')
            return redirect(next)
    
    return render_template('login.html',form=form)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("core.index"))


@auth.route('/account',methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateUserForm()
    if form.validate_on_submit():
        
        if form.email.data:
            current_user.email=form.email.data
        if form.password.data:
            current_user.password_hash = generate_password_hash(form.password.data)
        db.session.commit()
        flash('User account updated')
        return redirect(url_for('auth.account'))
    elif request.method=="GET":
        form.email.data=current_user.email
    return render_template('account.html',form=form)



# @auth.route('/enroll',methods=['GET', 'POST'])
# @login_required
# def enroll():
#     avail_courses=[a for a in Course.query.filter_by(can_apply=True).all() if a not in current_user.courses and current_user.branch.name in [b.name for b in a.branches] ]
#     not_eligible_courses=[a for a in Course.query.filter_by(can_apply=True).all() if a not in current_user.courses and current_user.branch.name not in [b.name for b in a.branches] and a not in current_user.requested_courses ]
#     requests = current_user.requests
#     if requests:
#         print(requests)
#     form = requestCourseForm()
#     if form.submit.data and form.validate:
#         attachments = []
#         if not current_user.is_authenticated:
#             abort(405)
#         newCourseNote = Request(current_user.id,form.course_id.data,form.title.data,form.details.data)
#         db.session.add(newCourseNote)
#         db.session.commit()

#         if form.attachments.data:
#             for uploaded_file in request.files.getlist('attachments'):

#                 filename, file_extension = os.path.splitext(
#                     uploaded_file.filename)
#                 if not filename or not file_extension:
#                     continue
            
#                 savename = secure_filename(filename)+''.join(
#                     random.choice(string.ascii_lowercase) for i in range(16))+file_extension
#                 print(filename, savename)
#                 if savename == "":
#                     break

#                 uploaded_file.save(os.path.join(
#                     basedir, '..', '..', 'static_material', savename))
#                 new_attachment = Attachment(
#                     filename, file_extension, url_for('course.serve_file', filename=savename), request_id=newCourseNote.id)
#                 attachments.append(new_attachment)
#         db.session.add_all(attachments)
#         db.session.commit()
#         return redirect(url_for('auth.enroll'))
    
#     return render_template('enroll.html', avail_courses=avail_courses, not_eligible_courses=not_eligible_courses, requestForm=form, requests=current_user.requests)


# @auth.route('/enroll/<course_id>')
# @login_required
# def enroll_course(course_id):
#     courseToAdd=Course.query.filter_by(id=course_id).first()
#     if courseToAdd is None or courseToAdd in current_user.courses:
#         flash("Course cannot be added")
#         abort(405)
#     current_user.courses.append(courseToAdd)
#     db.session.commit()
#     return redirect(url_for('core.index'))
    

# @auth.route('/request/<course_id>')
# @login_required
# def request_course(course_id):
#     courseToAdd = Course.query.filter_by(id=course_id).first()
#     if courseToAdd is None or courseToAdd in current_user.courses:
#         flash("Course cannot be added")
#         abort(405)
#     newRequest=Request(current_user.id,course_id)
#     db.session.add(newRequest)
#     db.session.commit()
#     return redirect(url_for('auth.enroll'))
