from app import app
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from flask_bcrypt import Bcrypt
from database import *
from forms import *



bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Students.query.get(int(user_id))


@login_manager.unauthorized_handler
def unauthorized():
    flash('Login required, please login in.', 'info')
    return redirect(url_for('login'))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))






@app.route('/', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
      
        user = Students.query.filter_by(student_id=form.student_id.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash('Login Successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check Student ID and Password', 'danger')
        return redirect(url_for('login'))
       

    return render_template('Home.html', title='Login', form=form)





@app.route('/profile', methods=['GET', 'POST'])
# @login_required
def profile():
    return render_template('profile.html', title='Profile')



@app.route('/borrow-book', methods=['GET', 'POST'])
# @login_required
def borrow_book():
    form = BorrowBook()
    
    if form.validate_on_submit():
        book = Library.query.filter_by(serial_no = form.serial_no.data, status='Available').first()
        if book:
            book.status = 'Borrowed'
            student = Students.query.filter_by(student_id=form.student_id.data).first()
            if not student:
                flash('Invalid Student ID', 'warning')
                return render_template('borrow_book.html', title='Borrow Book', form=form)
            borrow_book = Borrow(title=form.title.data, serial_no=form.serial_no.data, borrowed_by=form.student_id.data, status='Borrowed', student_name=student.name)
            
            db.session.add(borrow_book)

            db.session.commit()
            flash('Success', 'success')
            return redirect(url_for('profile'))
        else:
            flash("Book is Unavailable or Wrong Serial No.", 'warning')
            return render_template('borrow_book.html', title='Borrow Book', form=form)
        # return f"{form.title.data} {form.serial_no.data} {form.student_id.data}"
    return render_template('borrow_book.html', title='Borrow Book', form=form)



@app.route('/return-book', methods=['GET', 'POST'])
# @login_required
def return_book():
    form = ReturnBook()

    if form.validate_on_submit():
        book = Borrow.query.filter_by(serial_no=form.seral_no.data, borrowed_by=form.student_id.data, status='Borrowed').first()
        if book:
            book.status = 'Returned'
            book.returned_date = datetime.utcnow
            bk = Library.query.filter_by(serial_no=form.serial_no.data).frist()
            bk.status = 'Available'

            db.session.commit()

            flash('Success', 'success')
            return redirect(url_for('profile'))
        else:
            flash("Couldn't Find the required book. Check the serial no. and Student ID", 'warning')
            return render_template('return_book.html', title='Return Book', form=form)

    return render_template('return_book.html', title='Return Book', form=form)


@app.route('/view-borrowed-books', methods=['GET', 'POST'])
# @login_required
def view_borrowed_books():
    form = Search()
    books = Borrow.query.all()
    if form.validate_on_submit():
        books = Borrow.query.filter_by(title=form.search.data).all()
        return render_template('view-table.html', form=form, books=books)
    return render_template('view-table.html', title='View Borrowed Books', form=form, books=books)


@app.route('/view-students', methods=['GET', 'POST'])
def view_students():
    form = Search()
    if form.validate_on_submit():
        students = Students.query.all() 
    return render_template('view-students.html', form=form, students=students)



@app.route('/add-student', methods=['GET', 'POST'])
def add_student():
    form = AddStudent()
    if form.validate_on_submit():
        student = Students(name=form.name.data, student_id=form.student_id.data)
        db.session.add(student)
        db.session.commit()

        flash('Student Added Successfully')
        return redirect(url_for('profile'))
    return render_template('add-student.html', form=form, title='Add Student')