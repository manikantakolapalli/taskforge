from flask import Flask, render_template, request, redirect, url_for
import json, uuid
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'tasks.json'

def load_tasks():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add():
    tasks = load_tasks()
    new_task = {
        "id": str(uuid.uuid4()),
        "title": request.form['title'],
        "priority": request.form['priority'],
        "due_date": request.form['due_date'],
        "status": "Pending"
    }
    tasks.append(new_task)
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/complete/<task_id>')
def complete(task_id):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == task_id:
            task['status'] = "Completed"
    save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/delete/<task_id>')
def delete(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
