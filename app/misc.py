import re
from geopy import distance as dist

email_regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'

#TODO
def check_type(value, type, ref):
    if isinstance(value, type):
        return value
    else:
        return {'error': f'{ref} must be of type: number'}

def check_int(value, ref):
    try:
        value = int(value)
        return value
    except:
        return {'error': f'{ref} must be of type: number'}

def check_email(email):
    if(re.search(email_regex, email)):
        return True
    else:
        return False

def cdict(query, page=1, per_page=37):
    #TODO check that page and per_page are numbers
    resources = query.paginate(page, per_page, False)
    return {
        'items': [item.dict() for item in resources.items],
        'pages': resources.pages,
        'total': resources.total
    }