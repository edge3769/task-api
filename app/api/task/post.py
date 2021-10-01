from flask import request
from app.api import bp
from app.task_model import Task

@bp.route('/task', methods=['POST'])
def add_task():
    req_json = request.json.get
    name = req_json('name')
    task = req_json('task')
    child = req_json('child')
    if child:
        try:
            child = int(child)
        except:
            return {'error': 'child field should be an integer'}
        child = Task.query.get(child)
        if not child:
            return {'error': f'task to make child with id {child} was not found'}
    parent = req_json('parent')
    if parent:
        try:
            parent = int(parent)
        except:
            return {'error': 'parent field should be an integer'}
        parent = Task.query.get(parent)
        if not parent:
            return {'error': f'task to make parent with id {parent} was not found'}
    task = Task(name, parent)
    return task.dict()
