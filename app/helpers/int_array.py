def int_array(arr, name):
    for idx, num in enumerate(arr):
        try:
            arr[idx] = int(num)
        except:
            return {'error': f'specified {name} {num} does not seem to be a number'}, 400