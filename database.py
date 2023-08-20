from flask_sqlalchemy import SQLAlchemy
from app import app
from flask_login import UserMixin
from datetime import datetime
from flask_migrate import Migrate



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Students(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    form = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(60), unique=False, nullable=False)
    
    def __repr__(self):
        return '<Student %r>' % self.name

class Library(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=False, nullable=False)
    serial_no = db.Column(db.String(60), unique=True, nullable=False)
    status = db.Column(db.String(60), unique=False, nullable=False, default='Available')
    
    date = db.Column(db.String(20), unique=False, nullable=False, default=datetime.utcnow())
    
    def __repr__(self):
        return '<Book %r>' % self.title
    
class Borrow(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=False, nullable=False)
    serial_no = db.Column(db.String(60), unique=True, nullable=False)
    status = db.Column(db.String(60), unique=False, nullable=False)
    borrowed_by = db.Column(db.String(60), unique=False, nullable=False)
    student_name = db.Column(db.String(60), unique=False, nullable=False)
    borrowed_date = db.Column(db.String(20), unique=False, nullable=False, default=datetime.utcnow())
    returned_date = db.Column(db.String(20), unique=False, nullable=True)
    
    def __repr__(self):
        return '<Book %r>' % self.title