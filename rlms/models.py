# -*- coding: utf-8 -*-
# @Author: srajith
# @Date:   2020-06-16 18:36:35
# @Last Modified by:   srajith
# @Last Modified time: 2020-06-17 17:28:56
from rlms import db, login_manager
from datetime import datetime
from flask_login import UserMixin, current_user
from datetime import datetime

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	author = db.Column(db.String(200), nullable=False)
	description = db.Column(db.Text, nullable=True, default="No description available")
	available_books = db.Column(db.Integer, nullable=False)
	added_by = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return "{} by {}".format(self.title, self.author)

class BookLog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	book_id = db.Column(db.Integer, db.ForeignKey('book.id'))
	issued_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	issued_by = db.Column(db.Integer, nullable=False)
	borrower_id = db.Column(db.Integer, db.ForeignKey('student.id')) 
	def __repr__(self):
		return "id: {}, borrower: {}".format(self.id, self.borrower_details)

class Student(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	email = db.Column(db.Text, nullable=False)
	year = db.Column(db.String(10), nullable=False)
	branch = db.Column(db.String(20), nullable=False)
	books = db.relationship("BookLog", backref="borrower", lazy=True)

	def __repr__(self):
		return "{} -> {}".format(self.id, self.name) 

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String, nullable=False, unique=True)
	password = db.Column(db.String(60), nullable=False)

	def __repr__(self):
		return self.username

