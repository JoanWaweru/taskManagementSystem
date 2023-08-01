from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Task
from . import db
import json
import datetime
from datetime import datetime


views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    taskDate = datetime.strptime('2023-08-01', '%Y-%m-%d')
    if request.method == 'POST':
        taskTitle = request.form.get('taskTitle')
        taskDescription = request.form.get('taskDescription')
        taskDate = request.form.get('taskDate')
        taskStatus = request.form.get('taskStatus')

        if len(taskTitle) < 1:
            flash('Task is too short!', category='error')
        else:
            newTask = Task(
                taskTitle=taskTitle,
                taskDescription=taskDescription,
                taskDate=taskDate,
                taskStatus=taskStatus,
                user_id=current_user.id,
            )
            db.session.add(newTask)
            db.session.commit()
            flash('Task added!', category='success')

    return render_template('home.html', user=current_user)


@views.route('/deleteTask', methods=['POST'])
def delete_task():
    task = json.loads(request.taskTitle)
    taskId = task['taskId']
    task = Task.query.get(taskId)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()

    return jsonify({})
