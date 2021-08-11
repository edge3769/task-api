from flask import request
from app.api import bp
from app.misc import cdict, check_int
from app.decorators.req import req
from app.task_model import Task

@bp.route('/task', methods=['GET'])
def get():
#task arg:
    task = request.args.get('task')
    print('t', task)
    if task:
        try:
            task = int(task)
            task = Task.query.get(task)
        except: #TODO Exception type
            return {'error': 'task query argument must be a number type'} 
#id arg:    
    id = request.args.get('id')
    if id:
        try:
            id = int(id)
            return Task.query.get(id).dict()
        except: #TODO Exception type
            {'error': 'id query argument must be a number type'}
#page arg
    page = request.args.get('page')
    if page:
        try:
            page = int(page)
        except:
            return {'error': 'page query argument must be a number type'}
#per_page arg
    per_page = request.args.get('per_page')
    if per_page:
        try:
            per_page = int(per_page)
        except:
            return {'error': 'per_page query argument must be a number type'}
#search arg    
    search = request.args.get('q')
#depth arg
    depth = request.args.get('depth')
    if depth:
        if depth != 'all':
            try:
                depth = int(depth) 
                if depth != 1: #TODO accept any depth range
                    return {'error': "depth query argument must be the number '1' or string 'all'"}
            except:
                return {'error': "depth query argument must be the number '1' or string 'all'"}
#order arg
    order = request.args.get('order')
    if order:
        if order != 'asc' or order != 'dsc':
            return {'error': "order query argument must be either 'asc' or 'dsc'"}
#sort arg    
    sort = request.args.get('sort')
    if sort:
        if sort != 'time' or sort != 'alpha':
            return {'error': "sort query argument must be either 'time' or 'alpha'"}
#final return
    return cdict(Task.get(id, search, sort, order, task, depth), page, per_page)

@bp.route('/task', methods=['PUT'])
@req
def edit_task(req_json=None):
    print('.r: ', request.get_json)
    try:
        task = Task.query.get(req_json('id'))
        if not task:
            return {'error': 'task not found'}
    except:
        return {'error': 'id error'} #TODO
    
    add_tasks = req_json('add')
    remove_tasks = req_json('remove')
    
    # child tasks to remove from task
    if remove_tasks:
        if not isinstance(remove_tasks, list):
            return {'error': 'remove_tasks object is not an array type'}
        if not isinstance(add_tasks, list):
            return {'error': 'add_tasks object is not an array type'}
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
            added_tasks.append(_task.dict())
            task.add(_task)

    #task to add to task's parents    
    parent_id = req_json('parent')
    if parent_id:
        try:
            parent_id = int(parent_id)
            parent = Task.query.get(parent_id)
            if not parent:
                return {'error': f'task {parent_id} was not found'}
        except:
            return {'error': 'parent query arg must be of type: number'}
        parent.add(task)
    
    name = req_json('name') #TODO

    positions = req_json('position')
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
    
    done = req_json('done')
    if not isinstance(done, bool):
        return {'error': 'done value is not of type bool'}
    print('.r: done', done)
    
    data = {
        'name': name,
        'done': done,
    }
    task.edit(data)
    res = {
        'task': task.dict(),
        'added': added_tasks
    }
    return res, 202

@bp.route('/task', methods=['POST'])
def add_task():
    print('post')
    req_json = request.json.get
    name = req_json('name')
    task = req_json('task')
    print(name, task)
    if task:
        try:
            int(task)
        except:
            return {'error': 'task field should be an integer'}
    task = Task.query.get(task)
    task = Task(name, task)
    return task.dict()

@bp.route('/', methods=['DELETE'])
@req
def delete_task(req_json=None):
    id = req_json('id')
    task = Task.query.get(id)
    task.delete()
    return '', 202