from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from enum import Enum

class TaskStatus(Enum):
    PENDING = 'Pending'
    COMPLETED = 'Completed'

class Task(db.Model):
    taskId = db.Column(db.Integer, primary_key=True)
    taskTitle = db.Column(db.String(250))
    taskDescription = db.Column(db.Text)
    taskDate = db.Column(db.DateTime(timezone=True), default=func.now())
    taskStatus = db.Column(db.String(50), default=TaskStatus.PENDING.value)  # Use String type
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    # Convert Enum to String when storing in the database
    def __init__(self, *args, **kwargs):
        if 'taskStatus' in kwargs and isinstance(kwargs['taskStatus'], TaskStatus):
            kwargs['taskStatus'] = kwargs['taskStatus'].value
        super(Task, self).__init__(*args, **kwargs)

    # Convert String to Enum when retrieving from the database
    def __repr__(self):
        task_status = TaskStatus(self.taskStatus)
        return f"<Task {self.taskId}: {self.taskTitle} ({task_status})>"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    firstName = db.Column(db.String(150))
    tasks = db.relationship('Task', backref='user')
