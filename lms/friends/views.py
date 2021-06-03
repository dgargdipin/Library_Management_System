from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort,send_from_directory
from flask.globals import session
from flask_login import login_user, current_user, logout_user, login_required
from lms.models import User
from .forms import addFriendForm as aFF
from sqlalchemy import desc

from lms import db
friends = Blueprint('friends', __name__)

@friends.route('/friends/',methods=['GET', 'POST'])
@login_required
def all_following():
    addFriendForm=aFF()
    session['url']=url_for('friends.all_following')
    if addFriendForm.submit.data and addFriendForm.validate:
        user=User.query.filter_by(email=addFriendForm.email.data).first()
        if(user):
            current_user.following.append(user)
            db.session.commit()
        else:
            flash("Invalid email, user not found","warning")

    return render_template('friends.html',addFriendForm=addFriendForm)



@friends.route('/friends/<friend_id>')
@login_required
def friend_booklist(friend_id):
    friend=User.query.get(friend_id)

    if friend and friend in current_user.following:
        bookList=friend.reading_list
        session['url']=url_for('friends.friend_booklist',friend_id=friend_id)

    else:
        return 404
    return render_template('friend_booklist.html',booklist=bookList,friend=friend)


@friends.route('/friends/remove/<friend_id>')
@login_required
def remove_friend(friend_id):
    friend=User.query.get(friend_id)
    if friend and friend in current_user.following:
        current_user.following=[a for a in current_user.following if a.id!=friend.id]
        db.session.commit()
    return redirect(session['url'])