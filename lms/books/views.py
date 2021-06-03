from datetime import datetime
from lms.books.email import sendMail
from flask import Blueprint,session
from flask import render_template, url_for, flash, redirect, request, Blueprint, abort,send_from_directory
from flask_login import login_user, current_user, logout_user, login_required
from lms.models import Author, Book, Genre, Issues, Rating, Shelf
from .forms import NewBookForm, RatingForm, changeShelf, newShelf
from sqlalchemy import desc

from lms import db
books = Blueprint('books', __name__)

@books.route('/books/',methods=['GET', 'POST'])
@login_required
def all_books():
    allTheBooks=Book.query.all()
    newbookform=NewBookForm()
    reviewBookForm=RatingForm()
    newShelfForm=newShelf()
    chShelf=changeShelf()
    allshelfs=Shelf.query.all()
    session['url']=url_for('books.all_books')
    avg_genre=dict()
    genre_count=dict()
    for rating in current_user.ratings:
        for genre in rating.book.genres:
            avg_genre[genre.name]=avg_genre.get(genre.name,0)+rating.rating
            genre_count[genre.name]=genre_count.get(genre.name,0)+1
            

    for a in avg_genre:
        avg_genre[a]/=genre_count[a]

    maxGenre=list(avg_genre.keys())
    if maxGenre:
        maxGenre=maxGenre[0]
        for avgR in avg_genre:
            if(avg_genre[avgR]>avg_genre[maxGenre]):
                maxGenre=avgR
        suggestedBooks=Genre.query.filter_by(name=maxGenre).first().books
        print(suggestedBooks)
    else:
        suggestedBooks=None


    if newbookform.submitBook.data and newbookform.validate and current_user.isLibrarian:
        genreList=newbookform.genre.data.lower().split(",")
        genreObjectList=[]
        for genre in genreList:
            qResult=Genre.query.filter_by(name=genre.strip()).first()
            if qResult:
                genreObjectList.append(qResult)
            else:
                genreObjectList.append(Genre(name=genre.strip()))
                db.session.add(genreObjectList[-1])
        authorList=newbookform.authors.data.lower().split(',')
        authorObjectList=[]
        for author in authorList:
            qResult=Author.query.filter_by(name=author).first()
            if qResult:
                authorObjectList.append(qResult)
            else:
                authorObjectList.append(Author(name=author.strip()))
                db.session.add(authorObjectList[-1])
        shelfid=newbookform.shelf_id.data
        shelf=Shelf.query.get(shelfid)
        if not (shelf and len(shelf.books)<shelf.capacity) or Book.query.get(newbookform.isbn.data):
            flash("Not enough capacity.","warning")
            return redirect(url_for('books.all_books'))
        
        newBook=Book(name=newbookform.name.data,year=newbookform.year.data,url=newbookform.url.data,isbn=newbookform.isbn.data,copies=newbookform.copies.data,used=0,shelf_id=shelfid)
        newBook.genres=genreObjectList
        newBook.authors=authorObjectList
        db.session.add(newBook)
        db.session.commit()
        return redirect(url_for('books.all_books'))
    if reviewBookForm.submitRating.data and reviewBookForm.validate:
        newRating=Rating(
            user_id=current_user.id,
            isbn=reviewBookForm.isbn.data,
            rating=int(reviewBookForm.rating.data),
            review=reviewBookForm.review.data)
        db.session.add(newRating)
        db.session.commit()
        return redirect(url_for('books.all_books'))
    if chShelf.changeShelfSubmit.data and chShelf.validate and current_user.isLibrarian:
        shelfid=chShelf.shelfid.data
        book=Book.query.get(chShelf.isbn.data)
        if book and current_user.isLibrarian:
            shelf=Shelf.query.get(shelfid)
            if(shelf and len(shelf.books)<shelf.capacity):
                book.shelf_id=shelfid
                db.session.commit()
                flash("Shelf change was successful","primary")
            else:
                flash("Not enough capacity.","warning")

        return redirect(url_for('books.all_books'))
            
    if newShelfForm.newShelfSubmit.data and newShelfForm.validate and current_user.isLibrarian:
        shelfid=newShelfForm.shelfid.data
        shelf=Shelf.query.get(shelfid)
        if not shelf:
            s=Shelf(id=shelfid,capacity=newShelfForm.capacity.data)
            db.session.add(s)
            db.session.commit()
            flash("The new shelf was created.","primary")

        else:
            flash("The Shelf already exists","warning")
        return redirect(url_for('books.all_books'))
            
        

    return render_template('catalogue.html',suggested_books=suggestedBooks,shelfs=allshelfs,books=allTheBooks,newBookForm=newbookform,reviewBookForm=reviewBookForm,changeShelfForm=chShelf,newShelfForm=newShelfForm)




@books.route('/addtoreadinglist/<book_id>')
def add_to_reading_list(book_id):
    bk=Book.query.get(book_id)
    if bk:
        print("found book")
        current_user.reading_list.append(bk)
        db.session.commit()
        print(current_user.reading_list)
    if 'url' in session:
            return redirect(session['url'])
    return redirect(url_for('books.all_books'))



@books.route('/removefromreadinglist/<book_id>')
def remove_from_reading_list(book_id):
    bk=Book.query.get(book_id)
    if bk:
        print("found book")
        current_user.reading_list=[a for a in current_user.reading_list if a.isbn!=bk.isbn]
        print(current_user.reading_list)
        db.session.commit()
    if 'url' in session:
            return redirect(session['url'])
    return redirect(url_for('books.all_books'))



@books.route('/booksList/',methods=['GET'])
@login_required
def my_books():
    session['url']=url_for('books.my_books')
    return render_template('booklist.html',reading_list_ids=current_user.reading_list_ids)


@books.route('/issue/<book_id>')
@login_required
def issue_book(book_id):
    if (current_user.charges>=1000) or (len(current_user.books_issued)==3 and not current_user.isStaff):
        flash('Cannot issue more than 3 books at a time or your fine is too high.','danger')
    else:
        bk=Book.query.get(book_id)
        if bk and bk.used<bk.copies:
            newIssue=Issues(user_id=current_user.id,isbn=book_id)
            bk.used+=1
            db.session.add(newIssue)
            db.session.commit()
        else:
            flash('Book not found','danger')
    return redirect(url_for('books.all_books'))



@books.route('/hold/<book_id>')
@login_required
def hold_book(book_id):
    if (current_user.charges>=1000) or (len(current_user.books_issued)==3 and not current_user.isStaff):
        flash('Cannot hold if issued more than 3 books at a time.','danger')
    else:
        bk=Book.query.get(book_id)
        if bk and not bk.holder:
            current_user.holding.append(bk)
            db.session.commit()
            flash("Successfully put {} on hold".format(bk.name),"primary")
        else:
            flash('Book not found','danger')
    return redirect(url_for('books.all_books'))


@books.route('/removehold/<book_id>')
@login_required
def remove_hold_book(book_id):
    bk=Book.query.get(book_id)
    if bk and bk.holder==current_user:
        bk.holder=None
        db.session.commit()
        flash("Successfully removed from hold","primary")
    else:
        flash('Book not found','danger')
    return redirect(url_for('core.index'))


@books.route('/sendEmail/<issue_id>')
@login_required
def send_email(issue_id):
    issue=Issues.query.get(issue_id)
    if issue and not issue.returned:
        print(issue.user.email)
        sendMail(issue.user.email,issue.user.name,issue.bookIssued.name)
        issue.lastEmailSent=datetime.now()
        db.session.commit()
        flash('Email sent','primary')
    else:
        flash("Error","warning")
    return redirect(url_for('core.index'))



@books.route('/return/<issue_id>')
@login_required
def return_book(issue_id):
    
    
    a=Issues.query.get(issue_id)
    if a:
        a.returned=True
        bk=Book.query.get(a.isbn)
        if bk.holder:
            if not ((bk.holder.charges>=1000) or (len(bk.holder.books_issued)==3 and not bk.holder.isStaff)):
                newIssue=Issues(user_id=bk.holder.id,isbn=bk.isbn)
                db.session.add(newIssue)
                bk.holder=None
        else:
            bk.used-=1
        # a.bookIssued.used-=1
        # a.returned=True
        db.session.commit()

    else:
        flash('Book not found','danger')
    return redirect(url_for('core.index'))

