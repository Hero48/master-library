from app import app
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from flask_bcrypt import Bcrypt
from database import *
from forms import *
from sqlalchemy import func, or_
import pandas as pd
import os
from icecream import ic


bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


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
    if current_user.is_authenticated:
        return redirect(url_for('login_student'))
    form = LoginForm()
    if form.validate_on_submit():
      
        user = Admin.query.filter_by(admin_id=form.admin_id.data).first()
       
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash('Login Successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check Student ID and Password', 'danger')
        return redirect(url_for('login'))
       

    return render_template('Home.html', title='Login', form=form)





@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    total_borrowed_books = Borrow.query.count()
    total_students = Students.query.count()
    total_books = Library.query.count()
    active_students = Users.query.filter_by(active=True).count()
    return render_template('Dashboard.html', 
                           title='Dashboard', 
                           total_borrowed_books=total_borrowed_books, 
                           total_students=total_students, 
                           total_books=total_books,
                           active_students=active_students)




@app.route("/view-report", methods=["GET", "POST"])
@login_required
def view_report():
    form = ViewReport()
    if form.validate_on_submit():
        start_date=form.start_date.data
        end_date=form.end_date.data
        result = Users.query.filter(Users.entry_time.between(form.start_date.data, form.end_date.data)).all()
        total_books_available = Library.query.filter_by(status='Available').count()
        total_borrowed_books = Borrow.query.filter(Borrow.borrowed_date.between(start_date, end_date)).count()
        total_returned_books = Borrow.query.filter(Borrow.returned_date.between(start_date, end_date)).count()
        total_active_students = Users.query.filter(Users.entry_time.between(start_date, end_date)).distinct(Users.student_id).count()
        total_hours_spent = db.session.query(func.sum(Users.total_hours)).filter(Users.exit_time.between(start_date, end_date)).scalar()
        total_books = Library.query.count()

        return render_template("Report-table.html", 
                               start_date=form.start_date.data, 
                               end_date=form.end_date.data, 
                               total_books_available=total_books_available,
                               total_borrowed_books=total_borrowed_books,
                               total_returned_books=total_returned_books,
                               total_active_students=total_active_students,
                               total_hours_spent=total_hours_spent,
                               total_books = total_books)
    return render_template('Report-form.html', form=form, title="View Report")


@app.route('/borrow-book', methods=['GET', 'POST'])
@login_required
def borrow_book():
    form = BorrowBook()

    if form.validate_on_submit():
        book = Library.query.filter_by(serial_no=form.serial_no.data, status='Available').first()
        
        if book:
            book.status = 'Borrowed'
            student = Students.query.filter_by(student_id=form.student_id.data).first()
            
            if not student:
                flash('Invalid Student ID', 'warning')
                return render_template('Borrow-book.html', title='Borrow Book', form=form)
            
            borrow_book = Borrow(
                title=form.title.data, 
                serial_no=form.serial_no.data, 
                borrowed_by=form.student_id.data, 
                status='Borrowed', 
                student_name=student.name,
                author=book.author,
                publisher=book.publisher,
            )
            
            db.session.add(borrow_book)
            db.session.commit()
            flash('Success', 'success')
            return redirect(url_for('dashboard'))
        
        else:
            flash('Book is Unavailable or Wrong Serial No.', 'warning')
            return render_template('Borrow-book.html', title='Borrow Book', form=form)
    
    return render_template('Borrow-book.html', title='Borrow Book', form=form)



@app.route('/return-book', methods=['GET', 'POST'])
@login_required  
def return_book():
    form = ReturnBook()

    if form.validate_on_submit():
        book = Borrow.query.filter_by(serial_no=form.serial_no.data, borrowed_by=form.student_id.data, status='Borrowed').first()
        if book:
            book.status = 'Returned'
            book.returned_date = datetime.utcnow()
            bk = Library.query.filter_by(serial_no=form.serial_no.data).first()
            bk.status = 'Available'

            db.session.commit()

            flash('Success', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash("Couldn't Find the required book. Check the serial no. and Student ID", 'warning')
            return render_template('Return-book.html', title='Return Book', form=form)

    return render_template('Return-book.html', title='Return Book', form=form)


@app.route('/books-borrowed', methods=['GET', 'POST'])
@login_required
def books_borrowed():
    books = Borrow.query.all()
    total_borrowed_books = Borrow.query.count()
    total_returned_books = Borrow.query.filter_by(status='Returned').count()
  
    return render_template('Books-borrowed.html', title='Books Borrowed', books=books, total_borrowed_books=total_borrowed_books, total_returned_books=total_returned_books)




@app.route('/add-student', methods=['GET', 'POST'])
@login_required
def add_student():
    form = AddStudent()
    if form.validate_on_submit():
        
        student = Students(name=form.name.data, student_id=form.student_id.data, form=form.form.data)
        db.session.add(student)
        db.session.commit()
        flash('Student Added Successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('Register-student.html', form=form, title='Add Student')

@app.route('/register-admin', methods=['GET', 'POST'])
# TODO: make it login required before deployment
# @login_required
def register_admin():
    form = RegisterAdmin()
    if form.validate_on_submit():
        password = bcrypt.generate_password_hash(form.password.data)
        admin = Admin(name=form.name.data, admin_id=form.admin_id.data, password=password)
        db.session.add(admin)
        db.session.commit()
        print("\n here \n")
        flash('Admin Registered Successfully', 'success')
        return redirect(url_for('dashboard'))
    return render_template('Register-admin.html', form=form, title='Register Admin')

@app.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddBook()
    if form.validate_on_submit():
        existing_book = Library.query.filter_by(serial_no=form.book_id.data).first()
        if existing_book:
            flash("Book ID is already assigned")
            return redirect(url_for('add_book'))
        
        new_book = Library(
            title=form.book_title.data,
            serial_no=form.book_id.data,
            author=form.book_author.data,
            publisher=form.book_publisher.data,
            date_published=form.date_published.data,
            category=form.category.data,
            reference=form.reference.data,
            status='Available'
        )
        db.session.add(new_book)
        db.session.commit()

        flash('Book added successfully', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('Add-book.html', form=form, title='Add Book')


@app.route('/logout-student/<student_id>')
@login_required
def logout_student(student_id):
    student = Users.query.filter_by(student_id=student_id, active=True).first()
    if not student:
        flash('Active Student Not Available', 'info')
    student.exit_time = datetime.utcnow()
    exit_time_str = student.exit_time.strftime("%Y-%m-%d %H:%M:%S.%f")
    exit_time = datetime.strptime(exit_time_str, "%Y-%m-%d %H:%M:%S.%f")
    entry_time = datetime.strptime(student.entry_time, "%Y-%m-%d %H:%M:%S.%f")
    total_hours = (exit_time - entry_time).total_seconds() / 3600
    student.active = False
    student.total_hours = total_hours
    db.session.commit()
    flash(f'Successfully logged out {student.name}: {student.student_id}', 'success')
    return redirect(url_for('active_students'))


@app.route('/active-students')
@login_required
def active_students():
    students = Users.query.filter_by(active=True).all()
    active_students = Users.query.filter_by(active=True).count()
    return render_template('Active-students.html', title='Active Students', students=students, active_students=active_students)

@app.route('/login-student', methods=['GET', 'POST'])
@login_required
def login_student():
    form = LoginStudent()

    if form.validate_on_submit():
        ic(form.student_id.data)
        print("\n here \n")
        student = Students.query.filter_by(student_id=form.student_id.data).first()
        if not student:
            flash('Invalid student id', 'warning')
            return redirect(url_for('login_student'))
        user = Users.query.filter_by(student_id=form.student_id.data, active=True).first()
        if user :
            flash('Student is already logged in', 'warning')
            return redirect(url_for('login_student'))
        user = Users(name=student.name, student_id=student.student_id, form=student.form, active=True)
        db.session.add(user)
        db.session.commit()
        flash('Student Logged in successfully', 'success')
        return redirect(url_for('login_student'))

    return render_template('Login-student.html', form=form, title="Login Students")


@app.route('/search-student', methods=['GET', 'POST'])
@login_required
def search_student():
    form = SearchStudent()
    if form.validate_on_submit():
        search_query = form.search.data
        student = Students.query.filter(or_(
            Students.name.ilike(f'%{search_query}%'),
            Students.student_id.ilike(f'%{search_query}%')
        )).first()
        if not student:
            flash('No matching students found', 'warning')
            return redirect(url_for('search_student'))
        books_borrowed = Borrow.query.filter_by(borrowed_by=student.student_id).count()
        books_returned = Borrow.query.filter_by(borrowed_by=student.student_id, status='Returned').count()
        visit_count = Users.query.filter_by(student_id=student.student_id).count()
       
        return render_template(
            'Students-results.html',
            student=student,
            search=search_query,
            title="Search Students",
            books_borrowed=books_borrowed,
            books_returned=books_returned,
            visit_count=visit_count
        )
    return render_template('Search-student.html', form=form, title="Search Students")

@app.route("/search-book", methods=['GET', 'POST'])
def search_book():
    form = SearchBook()
    if form.validate_on_submit():
        search_query = form.search.data
        books = Library.query.filter(or_(Library.title.ilike(f'%{search_query}%'), Library.serial_no.ilike(f'%{search_query}%'))).all()
        total_books = Library.query.filter(or_(Library.title.ilike(f'%{search_query}%'), Library.serial_no.ilike(f'%{search_query}%'))).count()
        if not books:
            flash('No matching books found', 'warning')
            return redirect(url_for('search_book'))
        return render_template('Search-results.html', books=books, search=search_query, total_books=total_books, title="Search Books")
    return render_template('Search-book.html', form=form, title="Search Books")

@app.route('/all-books')
def all_books():
    books = Library.query.all()
    total_books = Library.query.count()
    return render_template('All-books.html', title='All Books', books=books, total_books=total_books)



@app.route('/upload-books', methods=['GET', 'POST'])
@login_required
def upload_books():
    form = UploadBooks()
    if form.validate_on_submit():
        file = form.file.data
        if file:
            df = pd.read_excel(file)
            try:

                for index, row in df.iterrows():
                    bk = Library.query.filter_by(serial_no=row['serial_no']).first()
                    if bk:
                        continue
                    book = Library(
                        title=row['title'],
                        serial_no=row['serial_no'],
                        author=row['author'],
                        publisher=row['publisher'],
                        date_published=row['date_published'],
                        category=row['category'],
                        reference=row['reference'],
                        status=row['status']
                    )
                    db.session.add(book)
            except:
                pass
            db.session.commit()
            flash('Books uploaded successfully', 'success')
            return redirect(url_for('dashboard'))
    return render_template('Upload-books.html', form=form, title="Upload Books")
























@app.route('/upload-students', methods=['GET', 'POST'])
@login_required
def upload_students():
    form = UploadStudents()
    if form.validate_on_submit():
        file = form.file.data
        if file:
            df = pd.read_excel(file)
            for index, row in df.iterrows():
                stnt = Students.query.filter_by(student_id=row['student_id']).first()
                if stnt:
                    continue
                student = Students(
                    name=row['name'],
                    student_id=row['student_id'],
                    form=row['form']
                )
                db.session.add(student)
            db.session.commit()
            flash('Students uploaded successfully', 'success')
            return redirect(url_for('dashboard'))
    return render_template('Upload-students.html', form=form, title="Upload Students")











@app.route("/spykvng/6542")
def reset_db():
    db.drop_all()
    db.create_all()
    db.session.commit()
    flash("Database Reset")
    return redirect(url_for('register_admin'))