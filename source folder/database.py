from flask_sqlalchemy import SQLAlchemy
from app import app
from flask_login import UserMixin
from datetime import datetime
from flask_migrate import Migrate



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    form = db.Column(db.String(20), unique=False, nullable=True)
   
    
    def __repr__(self):
        return '<Student %r>' % self.name
    

class Admin(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=True)
    admin_id = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=True)
    
    def __repr__(self):
        return '<Student %r>' % self.name
    

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=True)
    student_id = db.Column(db.String(20), unique=False, nullable=False)
    form = db.Column(db.String(20), unique=False, nullable=False)
    active = db.Column(db.String(60), unique=False, nullable=False)
    entry_time = db.Column(db.String(20), unique=False, nullable=False, default=datetime.utcnow())
    exit_time = db.Column(db.String(20), unique=False, nullable=True)
    total_hours = db.Column(db.Integer, unique=False, nullable=True)
    
    def __repr__(self):
        return '<Student %r>' % self.name

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=False, nullable=False)
    serial_no = db.Column(db.String(60), unique=True, nullable=False)
    author = db.Column(db.String(60), unique=False, nullable=False)
    publisher = db.Column(db.String(60), unique=False, nullable=False)
    date_published = db.Column(db.String(60), unique=False, nullable=False)
    status = db.Column(db.String(60), unique=False, nullable=False, default='Available')
    date = db.Column(db.String(20), unique=False, nullable=False, default=datetime.utcnow())
    category = db.Column(db.String(60), unique=False, nullable=False)
    reference = db.Column(db.String(60), unique=False, nullable=True)

    
    def __repr__(self):
        return '<Book %r>' % self.title
    
class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=False, nullable=False)
    serial_no = db.Column(db.String(60), unique=False, nullable=False)
    status = db.Column(db.String(60), unique=False, nullable=False)
    author = db.Column(db.String(60), unique=True, nullable=False)
    publisher = db.Column(db.String(60), unique=False, nullable=False)
    borrowed_by = db.Column(db.String(60), unique=False, nullable=False)
    student_name = db.Column(db.String(60), unique=False, nullable=False)

    borrowed_date = db.Column(db.String(20), unique=False, nullable=False, default=datetime.utcnow())
    returned_date = db.Column(db.DateTime, unique=False, nullable=True)
    
    def __repr__(self):
        return '<Book %r>' % self.title
