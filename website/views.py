from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Task
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        task = request.form.get('taskTitle')#Gets the task from the HTML 

        if len(task) < 1:
            flash('Task is too short!', category='error') 
        else:
            newTask = Task(taskDescription=task, user_id=current_user.id)  #providing the schema for the Task 
            db.session.add(newTask) #adding the Task to the database 
            db.session.commit()
            flash('Task added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/deleteTask', methods=['POST'])
def deleteTask():  
    task = json.loads(request.taskDescription) # this function expects a JSON from the INDEX.js file 
    taskId = task['taskId']
    task = Task.query.get(taskId)
    if task:
        if task.user_id == current_user.id:
            db.session.delete(task)
            db.session.commit()

    return jsonify({})