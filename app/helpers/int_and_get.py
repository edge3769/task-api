from . import int_array
from . import modelArray

def int_and_get(ids, Model, name):
    if ids:
        int_array(ids, name)
        print('ids', ids)
        modelArray(ids, Model, name)