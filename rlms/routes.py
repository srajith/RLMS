# -*- coding: utf-8 -*-
# @Author: srajith
# @Date:   2020-06-16 15:01:26
# @Last Modified by:   srajith
# @Last Modified time: 2020-06-18 13:14:07

from rlms import app, bcrypt, db
from flask import render_template, url_for, redirect, flash, request
from rlms.forms import *
from flask_login import login_required, current_user, login_user, logout_user
from rlms.models import *

@app.route("/")
@login_required
def index():
	return render_template('index.html')

@app.after_request
def add_header(r):
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response
# books 
@app.route("/books/add" ,methods=["GET", "POST"])
@login_required
def add_books():
	form = AddBooks()
	if form.validate_on_submit():
		book = Book(title=form.title.data, author=form.author.data, description=form.description.data, available_books=form.available_books.data, added_by=current_user.id)
		db.session.add(book)
		db.session.commit()
		flash("Successfully added !", "success")
		return redirect(url_for('all_books'))
	return render_template('add_books.html', form=form)

@app.route("/books")
@login_required
def all_books():
	books = Book.query.all()
	for book in books:
		book.added_name = User.query.filter_by(id=book.added_by).first().username
	total = len(books)
	return render_template('all_books.html', books=books)

@app.route("/books/return", methods=["GET", "POST"])
@login_required
def return_or_issue():
	issue_form =  IssueBooks()
	return_form = ReturnBooks()

	if issue_form.submit2.data and issue_form.validate_on_submit():
		if Student.query.filter_by(id=issue_form.student_id.data).first():
			book = Book.query.filter_by(id=issue_form.book_id.data).first()
			if book:
				if book.available_books > 0:
					book_log = BookLog(book_id=book.id, borrower_id=issue_form.student_id.data, issued_by=current_user.username)
					db.session.add(book_log)
					book = Book.query.filter_by(id=book_log.book_id).first()
					book.available_books -= 1
					db.session.commit()
					flash("Successfully issued book !", "success")
					return redirect(url_for('return_or_issue'))
				else:
					flash("Book unavailable", "info")
			else:
				flash("Invalid book id !", "danger")

		else:
			flash("Invalid student id !", "danger")


	if return_form.submit1.data and return_form.validate_on_submit():
		book_log = BookLog.query.filter_by(id=return_form.book_id.data).first()
		if book_log:
			db.session.delete(book_log)
			book = Book.query.filter_by(id=book_log.book_id).first()
			book.available_books += 1
			db.session.commit()
			return redirect(url_for('issued_books'))
		else:
			flash("Issue does not exist !", "danger")

	return render_template('return_or_issue.html', issue_form=issue_form, return_form=return_form)

@app.route("/all")
@login_required
def issued_books():
	book_logs = BookLog.query.all()
	for book_log in book_logs:
		book_log.title = Book.query.filter_by(id=book_log.book_id).first().title
		book_log.borrower_name = Student.query.filter_by(id=book_log.borrower_id).first().name
	return render_template('all_issued_books.html', book_logs=book_logs)

# students 

@app.route("/manage", methods=["GET", "POST"])
@login_required
def manage_students():
	form = AddStudents()
	del_form = DeleteStudent()

	if form.submit1.data and form.validate_on_submit():
		student = Student(name=form.name.data, email=form.email.data, year=form.year.data, branch=form.branch.data)
		db.session.add(student)
		db.session.commit()
		flash("Successfully added student", "success")
		return redirect(url_for('all_students'))

	if del_form.submit2.data and del_form.validate_on_submit():
		student = Student.query.filter_by(id=del_form.id.data).first()
		if student:
			db.session.delete(student)
			db.session.commit()
			flash("Successfully deleted student", "info")
			return redirect(url_for('all_students'))
		else:
			flash("Invalid student id", "warning")

	return render_template('manage_students.html', form=form, del_form=del_form)

@app.route("/students")
@login_required
def all_students():
	students = Student.query.all()
	return render_template('all_students.html', students=students)

# login 

@app.route("/register", methods=["GET", "POST"])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = Register()
	if form.validate_on_submit():
		hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
		user = User(username=form.username.data, password=hashed_pw)
		db.session.add(user)
		db.session.commit()
		return redirect(url_for("login"))

	return render_template('register.html', form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = Login()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user)
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('index')) 
		else:
			flash("Invalid credentials !", "danger")
			# return redirect(url_for('login'))
	return render_template('login.html', form=form)

@app.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('login'))
