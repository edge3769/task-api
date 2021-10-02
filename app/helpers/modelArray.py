def model_array(arr, Model, name):
    for idx, id in enumerate(arr):
        try:
            item = Model.query.get(id)
            if not item:
                return {'error': f'error finding {name} with id {id}'}, 400
            arr[idx] = item
        except:
            return {'error': f'error finding {name} with id {id}'}, 400