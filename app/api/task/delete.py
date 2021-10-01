from flask import request
from app.api import bp
from app.task_model import Task

@bp.route('/task', methods=['DELETE'])
def delete_task():
    id = request.args.get('id')
    try:
        id = int(id)
    except:
        return {'error': f'{id} does not seem to be a number, please provide a number id'}
    task = Task.query.get(id)
    if not task:
        return {'error': f'task with provided id {id} was not found'}
    task.delete()
    return {'ok': True}, 202