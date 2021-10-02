import json
from flask import request
from app.api import bp
from app.misc import cdict
from app.task_model import Task

@bp.route('/task', methods=['GET'])
def get():
#id arg:
    id = request.args.get('id')
    if id:
        try:
            id = int(id)
            _task = Task.query.get(id).dict()
            if not _task:
                return {'error': f'task with id {id} was not found'}, 400
        except: 
            return {'error': '"id" query argument must be a number'}, 400
    else:
        _task = None
# parents arg:
    parents = request.args.get('parents')
    _parents = []
    not_string_array_error = '"parents" query argument does not seem to be a stringified array'
    if parents:
        try:
            parents = json.loads(parents)
        except:
            return {'error': not_string_array_error}, 400
        if not isinstance(parents, list):
            return {'error': not_string_array_error}, 400
        errors = []
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
            _parents.append(parent_id)
        if len(unfound):
            errors.append(f'tasks with ids {unfound} were not found')
        if len(not_numbers):
            errors.append(f'provided ids {not_numbers} are not numbers')
        if len(errors):
            return {'errors': errors}, 400
#page arg
    page = request.args.get('page')
    if page:
        try:
            page = int(page)
        except:
            return {'error': 'page query argument must be a number type'}, 400
#per_page arg
    per_page = request.args.get('per_page')
    if per_page:
        try:
            per_page = int(per_page)
        except:
            return {'error': 'per_page query argument must be a number type'}, 400
#search arg    
    search = request.args.get('q')
#depth arg
    depth = request.args.get('depth')
    if depth:
        if depth != 'all':
            try:
                depth = int(depth) 
                if depth != 1: #TODO accept any depth range
                    return {'error': "depth query argument must be the number '1' or string 'all'"}, 400
            except:
                return {'error': "depth query argument must be the number '1' or string 'all'"}, 400
#order arg
    order = request.args.get('order')
    if order:
        if order != 'asc' or order != 'dsc':
            return {'error': "order query argument must be either 'asc' or 'dsc'"}, 400
#sort arg    
    sort = request.args.get('sort')
    if sort:
        if sort != 'time' or sort != 'alpha':
            return {'error': "sort query argument must be either 'time' or 'alpha'"}, 400
#final return
    res = {
        'children': cdict(Task.get(None, _parents, search, sort, order, depth), page, per_page),
        'parents': cdict(Task.get(id, None, search, sort, order, depth), page, per_page),
    }
    if _task:
        res['task'] = _task
    return res