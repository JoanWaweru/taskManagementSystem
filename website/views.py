from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Task
from . import db
import datetime

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST', 'PUT'])
@login_required
def home():
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
def deleteTask():
    data = request.get_json()
    taskId = data.get('taskId')
    task = Task.query.get(taskId)
    if task and task.user_id == current_user.id:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted!', category='success')
    else:
        flash('Task not found or not allowed to delete!', category='error')

    return jsonify({})

@views.route('/updateTask', methods=['PUT'])
def updateTask():
    if request.method == 'PUT':
        taskId = request.form.get('taskId')
        taskTitle = request.form.get('taskTitle')
        taskDescription = request.form.get('taskDescription')
        taskDate = request.form.get('taskDate')
        taskStatus = request.form.get('taskStatus')

        if len(taskTitle) < 1:
            flash('Task is too short!', category='error')
        else:
            task = Task.query.get(taskId)
            if task is None:
                flash('Task not found!', category='error')
            else:
                task.taskTitle = taskTitle
                task.taskDescription = taskDescription
                task.taskDate = taskDate
                task.taskStatus = taskStatus
                db.session.commit()
                flash('Task updated!', category='success')

    return jsonify({})

