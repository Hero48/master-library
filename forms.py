from app import app
from  flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, equal_to, Length



#login form

class LoginForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BorrowBook(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    title = StringField("Book's Title", validators=[DataRequired()])
    serial_no = StringField("Book's Serial No.", validators=[DataRequired()])
    submit = SubmitField('Submit')

class ReturnBook(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    title = StringField("Book's Title", validators=[DataRequired()])
    serial_no = StringField("Book's Serial No.", validators=[DataRequired()])
    submit = SubmitField('Submit')

class Search(FlaskForm):
    search = StringField('Search', validators=[DataRequired()])
    submit = SubmitField('submit')


class AddStudent(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    name = StringField('Student Name', validators=[DataRequired()])
    form = StringField('Student Form', validators=[DataRequired()])
    password = StringField('Enter New Password ', validators=[DataRequired()])
    submit = SubmitField('Add Sutdent')

class AddBook(FlaskForm):
    book_id = StringField('Book ID', validators=[DataRequired()])
    book_title = StringField('Book Title', validators=[DataRequired()])
    
    submit = SubmitField('Add Book')
