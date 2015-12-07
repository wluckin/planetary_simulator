import collections

def is_number(x):
    """ Does this need a docstring """
    try:
        float(x)
        return True
    except ValueError:
        return False

def convert(data):
    if isinstance(data, basestring):
        return str(data)
    elif isinstance(data, collections.Mapping):
        return dict(map(convert, data.iteritems()))
    elif isinstance(data, collections.Iterable):
        return type(data)(map(convert, data))
    else:
        return data
