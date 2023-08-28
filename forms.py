from app import app
from  flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, equal_to, Length



#login form

class LoginForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired(), Length(min=8, max=10)])
    password = StringField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class BorrowBook(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired(), Length(min=8, max=10)])
    title = StringField("Book's Title", validators=[DataRequired()])
    serial_no = StringField("Book's Serial No.", validators=[DataRequired(), Length(min=4, max=20)])
    submit = SubmitField('Submit')

class ReturnBook(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired(), Length(min=8, max=10)])
    serial_no = StringField("Book's Serial No.", validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginStudent(FlaskForm):
    student_id = StringField('Login Student', validators=[DataRequired(), Length(min=8, max=10)])
    submit = SubmitField('submit')
class Search(FlaskForm):
    search = StringField('Login Student', validators=[DataRequired(), Length(min=8, max=10)])
    submit = SubmitField('submit')


class AddStudent(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired(), Length(min=8, max=10)])
    name = StringField('Student Name', validators=[DataRequired()])
    form = StringField('Student Form', validators=[DataRequired()])
    password = StringField('Enter New Password ')
    submit = SubmitField('Add Sutdent')

class AddBook(FlaskForm):
    book_id = StringField('Book ID', validators=[DataRequired()])
    book_title = StringField('Book Title', validators=[DataRequired(), Length( min=4, max=20)])
    
    submit = SubmitField('Add Book')
