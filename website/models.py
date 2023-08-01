from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class Task(db.Model):
    taskId = db.Column(db.Integer, primary_key = True)
    taskTitle = db.Column(db.String(250))
    taskDescription = db.Column(db.Text)
    taskDate = db.Column(db.DateTime(timezone=True), default=func.now())
    taskStatus =db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    #def __repr__(self):
        #return f"<Task {self.taskId}: {self.taskTitle} ({self.taskStatus})>"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    tasks = db.relationship('Task')