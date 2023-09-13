from app import app
from flask import render_template, url_for, redirect, flash, request
from flask_login import login_user, logout_user, login_required, LoginManager, current_user
from flask_bcrypt import Bcrypt
from database import *
from forms import *
from sqlalchemy import func



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
    if current_user.is_authenticated:
        return redirect(url_for('login_student'))
    form = LoginForm()
    if form.validate_on_submit():
      
        user = Students.query.filter_by(student_id=form.student_id.data).first()
        if user.password == None:
            flash('Invalid student id or password', 'warning')
            return redirect(url_for('login'))
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=True)
            next_page = request.args.get('next')
            flash('Login Successful', 'success')
            return redirect(next_page) if next_page else redirect(url_for('profile'))
        else:
            flash('Login Unsuccessful. Please check Student ID and Password', 'danger')
        return redirect(url_for('login'))
       

    return render_template('Home.html', title='Login', form=form)





@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def profile():
    total_borrowed_books = Borrow.query.count()
    total_students = Students.query.count()
    total_books = Library.query.count()
    return render_template('profile.html', 
                           title='Dashboard', 
                           total_borrowed_books=total_borrowed_books, 
                           total_students=total_students, 
                           total_books=total_books)




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

        return render_template("report-table.html", 
                               start_date=form.start_date.data, 
                               end_date=form.end_date.data, 
                               total_books_available=total_books_available,
                               total_borrowed_books=total_borrowed_books,
                               total_returned_books=total_returned_books,
                               total_active_students=total_active_students,
                               total_hours_spent=total_hours_spent)
    return render_template('view-report.html', form=form, title="View Report")


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
                return render_template('borrow_book.html', title='Borrow Book', form=form)
            
            borrow_book = Borrow(
                title=form.title.data, 
                serial_no=form.serial_no.data, 
                borrowed_by=form.student_id.data, 
                status='Borrowed', 
                student_name=student.name,
                author=book.author,
                pubisher=book.pubisher,
            )
            
            db.session.add(borrow_book)
            db.session.commit()
            flash('Success', 'success')
            return redirect(url_for('profile'))
        
        else:
            flash('Book is Unavailable or Wrong Serial No.', 'warning')
            return render_template('borrow_book.html', title='Borrow Book', form=form)
    
    return render_template('borrow_book.html', title='Borrow Book', form=form)



@app.route('/return-book', methods=['GET', 'POST'])
@login_required
def return_book():
    form = ReturnBook()
    print(form.serial_no.data, form.student_id.data)

    if form.validate_on_submit():
        book = Borrow.query.filter_by(serial_no=form.serial_no.data, borrowed_by=form.student_id.data, status='Borrowed').first()
        if book:
            book.status = 'Returned'
            book.returned_date = datetime.utcnow()
            bk = Library.query.filter_by(serial_no=form.serial_no.data).first()
            bk.status = 'Available'

            db.session.commit()

            flash('Success', 'success')
            return redirect(url_for('profile'))
        else:
            flash("Couldn't Find the required book. Check the serial no. and Student ID", 'warning')
            return render_template('return_book.html', title='Return Book', form=form)

    return render_template('return_book.html', title='Return Book', form=form)


@app.route('/view-borrowed-books', methods=['GET', 'POST'])
@login_required
def view_borrowed_books():
    form = Search()
    books = Borrow.query.all()
    if form.validate_on_submit():
        books = Borrow.query.filter_by(title=form.search.data).all()
        return render_template('view-table.html', form=form, books=books)
    return render_template('view-table.html', title='View Borrowed Books', form=form, books=books)


# @app.route('/view-students', methods=['GET', 'POST'])
# @login_required
# def view_students():
#     form = Search()
#     students = Students.query.all() 
#     if form.validate_on_submit():
#         students = Students.query.filter_by(student_id=form.search.data).all()

#         return render_template('view-students.html', form=form, students=students)
#     return render_template('view-students.html', form=form, students=students)
 


@app.route('/add-student', methods=['GET', 'POST'])
@login_required
def add_student():
    form = AddStudent()
    if form.validate_on_submit():
        if form.password.data:
            password = bcrypt.generate_password_hash(form.password.data)
            student = Students(name=form.name.data, student_id=form.student_id.data, password=password, form=form.form.data)
            db.session.add(student)
            db.session.commit()
            flash('Student Added Successfully', 'success')
            return redirect(url_for('profile'))
        else:
            student = Students(name=form.name.data, student_id=form.student_id.data, form=form.form.data)
            db.session.add(student)
            db.session.commit()
            flash('Student Added Successfully', 'success')
            return redirect(url_for('profile'))
    return render_template('add-student.html', form=form, title='Add Student')

@app.route('/add-book', methods=['GET', 'POST'])
@login_required
def add_book():
    form = AddBook()
    if form.validate_on_submit():
        book = Library(title=form.book_title.data, serial_no=form.book_id.data, author=form.book_author.data, publisher=form.book_publisher.data)
        db.session.add(book)
        db.session.commit()

        flash('Book added successfully', 'success')
        return redirect(url_for('profile'))
    return render_template('add-book.html', form=form, title='Add Book')


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
    return render_template('active_students.html', title='Active Students', students=students)

@app.route('/login-student', methods=['GET', 'POST'])
@login_required
def login_student():
    form = LoginStudent()

    if form.validate_on_submit():
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

    return render_template('login-student.html', form=form, title="Login Students")
