from flask import request
from app.helpers import int_and_get
from app.api import bp
from app.task_model import Task

@bp.route('/task', methods=['PUT'])
def edit_task():
    req_data = request.json.get
    tasks = int_and_get(req_data('tasks'), Task, 'task')
    addChildren = int_and_get(req_data('addChildren'), Task, 'child')
    removeChildren = int_and_get(req_data('removeChildren'), Task, 'child')
    addParents = int_and_get(req_data('addParents'), Task, 'parent')
    removeParents = int_and_get(req_data('removeParents'), Task, 'parent')

    add_tasks = req_data('add')
    remove_tasks = req_data('remove')
    
    # child tasks to remove from task
    if remove_tasks:
        if not isinstance(remove_tasks, list):
            return {'error': 'remove_tasks object is not an array type'}
        for id in remove_tasks:
            _task = Task.query.get(id)
            if not _task:
                return {'error': f'task {id} was not found'}
            task.remove(_task)
    
    # tasks to add to task's children
    added_tasks = []
    if add_tasks:
        if not isinstance(add_tasks, list):
            return {'error': 'add body parameter must be of type: array'}
        for id in add_tasks:
            _task = Task.query.get(id)
            if not _task:
                return {'error': f'task {id} was not found'}
            task.add(_task)
            added_tasks.append(_task.dict())

    #task to add to task's parents   
    parents = request.args.get('parents')
    if parents:
        if not isinstance(parents, list):
            return {'error': '"parents" query argument must be a stringified array'}
        unfound = ''
        not_numbers = ''
        for parent_id in parents:
            try:
                parent_id = int(parent_id)
            except:
                not_numbers.join(f'{parent_id}, ')
                continue
            parent_task = Task.query.get(parent_id)
            if not parent_task:
                unfound.join(f'{parent_id}, ')
                continue
            parent_task.add(task)
        # There are no spaces after the variable in the f-string because spaces were added when each id was added
        errors = []
        if len(not_numbers):
            errors.append(f'the following provided ids: {not_numbers}are not numbers')
        if len(unfound):
            errors.append(f'tasks with ids {unfound}were not found')
        if len(errors) > 1:
            return {'errors': errors}
        else:
            if len(not_numbers):
                return {'error': f'the following provided ids: {not_numbers}are not numbers'}
            if len(unfound):
                return {'error': f'tasks with ids {unfound}were not found'}
    name = req_data('name') #TODO

    #postion parameter
    positions = req_data('position')
    if positions:
        if not isinstance(positions, list):
            return {'error': '"position" body parameter must be of type: array'}
        for position_obj in positions:
            if not isinstance(position_obj, dict):
                return {'error': 'values in "position" body parameter must be of type: object'}
            try:
                parent_id = int(position_obj['parent'])
            except:
                return {'error': 'parent attribute of value in "position" body parameter must be of type: number'}
            try:
                position = int(position_obj['position'])
            except:
                return {'error': 'position attribute of value in "position" body parameter must be of type: number'}
            
            parent = Task.query.get(parent_id)
            parent.add(task)
            task.set_child_position(parent, position)

    #shift parameter
    shift = req_data('shift')
    if shift:
        direction = None
        parent = None
        if not isinstance(shift, dict):
            return {'error': '"shift" body parameter must be of type: object'}
        if 'direction' in shift:
            direction = shift['direction']
            if not isinstance(direction, bool):
                return {'error': '"direction" attribute of "shift" body parameter must be of type: bool'}
        if 'parent' in shift:
            parent_id = shift['parent']
            try:
                parent_id = int(parent_id)
            except:
                return {'error': '"parent" attribute of "shift" body parameter must be of type: number'}
            parent = Task.query.get(parent_id)
            if not parent:
                return {'error': f'task with id {parent_id} was not found'}
        if not direction:
            return {'error': f'a "direction" attribute was not specified in the shift body parameter'}
        task.shift(direction, parent)
    
    done = req_data('done')
    if done:
        if not isinstance(done, bool):
            return {'error': 'done value is not of type bool'}
    
    data = {
        'name': name,
        'done': done,
    }
    task.edit(data)
    res = {
        'ok': True,
        'task': task.dict(),
        'added': added_tasks
    }
    return res, 202