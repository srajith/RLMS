# -*- coding: utf-8 -*-
# @Author: srajith
# @Date:   2020-06-16 15:32:31
# @Last Modified by:   srajith
# @Last Modified time: 2020-06-17 17:45:12
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class Login(FlaskForm):
	
	username = StringField("Username", validators=[DataRequired(), Length(min=5)])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
	remember = BooleanField('Remember Me')	
	submit = SubmitField("Login")

class Register(FlaskForm):
	
	username = StringField("Username", validators=[DataRequired(), Length(min=5)])
	password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
	confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=8), EqualTo('password')])
	submit = SubmitField("Register")


class AddBooks(FlaskForm):
	
	title = StringField("Title", validators=[DataRequired(), Length(min=5, max=50)])
	author = StringField("Author", validators=[DataRequired(), Length(min=5, max=100)])
	description = TextAreaField("Description")
	available_books = IntegerField("No of Books" ,validators=[DataRequired("Please enter a number !")])
	submit = SubmitField("Add book")
	
class ReturnBooks(FlaskForm):
	
	book_id = IntegerField("Issue id", validators=[DataRequired()]) 
	submit1 = SubmitField("Return Book")

class IssueBooks(FlaskForm):
	
	book_id = IntegerField("Book id", validators=[DataRequired()]) 
	student_id = IntegerField("Student id", validators=[DataRequired()]) 
	submit2 = SubmitField("Issue Book")


class AddStudents(FlaskForm):
	
	name = StringField("Name", validators=[DataRequired(), Length(min=5, max=50)])
	email = StringField("Email", validators=[DataRequired(), Email()])
	year = SelectField('Year', choices=[('First', 'First'), ('Second', 'Second'), ('Third', 'Third')])
	branch = SelectField('Branch', choices=[('CSC', 'CSC'), ('BCS', 'BCS'), ('BES', 'BES')])
	submit1 = SubmitField("Add Student")

class DeleteStudent(FlaskForm):
	
	id = IntegerField("Student id", validators=[DataRequired()])
	submit2 = SubmitField("Delete")