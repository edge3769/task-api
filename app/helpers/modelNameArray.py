def model_array(arr, Model, name):
    for idx, n in enumerate(arr):
            arr[idx] = Model.c(n)