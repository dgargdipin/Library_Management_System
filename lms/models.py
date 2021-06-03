from enum import unique

from sqlalchemy.orm import backref
# from werkzeug.wrappers import UserM
# from cms.core.views import index
from lms import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class Rating(db.Model):
    __tablename__='ratings'
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'), primary_key=True)
    isbn=db.Column(db.String,db.ForeignKey('books.isbn'), primary_key=True)
    rating=db.Column(db.Integer,nullable=False)
    review=db.Column(db.String(100))
    on=db.Column(db.DateTime,default=datetime.datetime.now())


user_to_user = db.Table('user_to_user',
    db.Column("follower_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("followed_id", db.Integer, db.ForeignKey("users.id"), primary_key=True)
)

reading_list = db.Table('reading_list',
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("books.isbn"), primary_key=True)
)



class User(db.Model,UserMixin):
    __tablename__='users'
    name=db.Column(db.String(),nullable=False)
    id=db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),unique=True,index=True)
    password=db.Column(db.String(128))
    # checkedOutBooks=db.relationship('Book', backref='currUser')
    ratings=db.relationship('Rating',backref='user')
    following = db.relationship("User",
                    secondary=user_to_user,
                    primaryjoin=id==user_to_user.c.follower_id,
                    secondaryjoin=id==user_to_user.c.followed_id,
                    backref="followed_by"
    )
    reading_list=db.relationship('Book',secondary=reading_list)
    issued=db.relationship('Issues',backref='user')
    isLibrarian=db.Column(db.Boolean,default=False)
    isStaff=db.Column(db.Boolean,default=False)
    about=db.Column(db.String)
    holding = db.relationship("Book",backref='holder', foreign_keys='Book.holder_id')
    @property
    def charges(self):
        charge=0
        for issue in self.issued:
            if not issue.returned and datetime.datetime.now()>issue.dueDate:
                delta=datetime.datetime.now()-issue.dueDate
                charge+=delta.days*10
        return charge

    @property
    def reading_list_ids(self):
        ret=[int(a.isbn) for a in self.reading_list]
        print(ret)
        return ret
    @property
    def issued_book_ids(self):
        ret=[int(a.bookIssued.isbn) for a in self.issued if not a.returned]
        print(ret)
        return ret
    @property
    def books_issued(self):
        return[a.bookIssued for a in self.issued if not a.returned]
    @property
    def rated_book_ids(self):
        return [a.book.isbn for a in self.ratings]
    @property
    def active_issues(self):
        return [a for a in self.issued if not a.returned]
    @property
    def hold_book_ids(self):
        print(self.holding)
        return [a.isbn for a in self.holding]

    def check_password(self,password):
        return check_password_hash(self.password,password)



class Issues(db.Model):
    __tablename__='issues'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    isbn=db.Column(db.String,db.ForeignKey('books.isbn') )
    issue_date=db.Column(db.DateTime,default=datetime.datetime.now(),nullable=False)
    dueDate=db.Column(db.DateTime,default=datetime.datetime.now()+datetime.timedelta(days=30),nullable=False)
    returned=db.Column(db.Boolean,default=False)
    lastEmailSent=db.Column(db.DateTime)
    @property
    def fine(self):
        return max(0,((datetime.datetime.now()-self.dueDate).days)*10) 



author_table = db.Table('author_table',
    db.Column("author_id", db.Integer, db.ForeignKey("authors.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("books.isbn"), primary_key=True)
)


genre_table = db.Table('genre_table',
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id"), primary_key=True),
    db.Column("book_id", db.Integer, db.ForeignKey("books.isbn"), primary_key=True)
)

class Book(db.Model):
    __tablename__='books'
    name=db.Column(db.String(),nullable=False)
    isbn=db.Column(db.Integer,primary_key=True)
    copies=db.Column(db.Integer,default=1,nullable=False)
    used=db.Column(db.Integer,default=0,nullable=False)
    ratings=db.relationship('Rating',backref='book')
    authors = db.relationship('Author', secondary=author_table,backref=db.backref('books'))
    genres = db.relationship('Genre', secondary=genre_table,backref=db.backref('books'))
    shelf_id= db.Column(db.Integer, db.ForeignKey('shelfs.id'))
    issues=db.relationship('Issues',backref='bookIssued',uselist=False)
    year=db.Column(db.Integer,default=2021)
    url=db.Column(db.String,default="https://s3.eu-central-1.amazonaws.com/bootstrapbaymisc/blog/24_days_bootstrap/don_quixote.jpg")
    holder_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    @property
    def avg_rating(self):
        if not self.ratings:
            return 5
        ans=0
        for rating in self.ratings:
            ans+=rating.rating
        
        ans=ans/len(self.ratings)
        return ans

class Genre(db.Model):
    __tablename='genre'
    id=db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(), nullable = False)

class Author(db.Model):
    __tablename__ = 'authors'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(), nullable = False)
    def __repr__(self) -> str:
        return self.name.strip().capitalize()

class Shelf(db.Model):
    __tablename__ = 'shelfs'
    id = db.Column(db.Integer, primary_key = True)
    capacity = db.Column(db.Integer, nullable = False)
    currHolding=db.Column(db.Integer, nullable = False,default=0)
    books = db.relationship('Book',backref='shelf')



class Customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)


    billing_address = db.relationship("Address", foreign_keys='Address.billing_address_id')
    shipping_address = db.relationship("Address", foreign_keys='Address.shipping_address_id')

class Address(db.Model):
    __tablename__ = 'address'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)
    shipping_address_id = db.Column(db.Integer, db.ForeignKey("customer.id"))
    billing_address_id = db.Column(db.Integer, db.ForeignKey("customer.id"))

