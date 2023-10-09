from app import app
from  flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TextAreaField, DateField
from wtforms.validators import DataRequired, EqualTo, Length



#login form

class LoginForm(FlaskForm):
    admin_id = StringField('Student ID', validators=[DataRequired(), Length(min=8, max=10)])
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
    submit = SubmitField('Add Sutdent')


class RegisterAdmin(FlaskForm):
    admin_id = StringField('Admin ID', validators=[DataRequired(), Length(min=8, max=10)])
    name = StringField('Admin Name', validators=[DataRequired()])
    password = StringField('Enter New Password ', validators=[DataRequired(), Length(min=4, max=20)])
    confirm_password = StringField("Confrim Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register Admin')

class AddBook(FlaskForm):
    book_id = StringField('Book ID', validators=[DataRequired()])
    book_title = StringField('Book Title', validators=[DataRequired(), Length( min=4, max=20)])
    book_author = StringField('Book Author', validators=[DataRequired(), Length( min=4, max=20)])
    book_publisher = StringField('Book Publisher', validators=[DataRequired(), Length( min=4, max=20)])
    date_published = DateField("Enter Published Date", validators=[DataRequired()])
    
    submit = SubmitField('Add Book')


class ViewReport(FlaskForm):
    start_date = DateField("Choose Start Date", validators=[DataRequired()])
    end_date = DateField("Choose End Date", validators=[DataRequired()])
    submit = SubmitField('Submit')
    

class SearchStudent(FlaskForm):
    search = StringField('Search Student', validators=[DataRequired()])
    submit = SubmitField('submit')

class SearchBook(FlaskForm):
    search = StringField('Search Book', validators=[DataRequired()])
    submit = SubmitField('submit')