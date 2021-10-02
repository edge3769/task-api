from . import int_array
from . import modelArray

def int_and_get(ids, Model, name):
    int_array(ids, name)
    console.log('ids', ids)
    modelArray(ids, Model, name)