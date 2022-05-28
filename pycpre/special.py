def cembed(o):
    if isinstance(o, int) or isinstance(o, float):
        return str(o)
    elif isinstance(o, str):
        return "\"{}\"".format(o)
    elif isinstance(o, list):
        return "{{{}}}".format(", ".join(cembed(x) for x in o))
    else:
        return o.__cembed__()


def cdeps(o):
    if isinstance(o, int) or isinstance(o, float) or isinstance(o, str):
        return []
    elif isinstance(o, list):
        r = []
        for x in o:
            r.extend(cdeps(x))
        return list(r)
    else:
        return o.__cdeps__()


def cbuild(o):
    if isinstance(o, int) or isinstance(o, float) or isinstance(o, str):
        return None
    elif isinstance(o, list):
        return list(cbuild(x) for x in o)
    else:
        return o.__cbuild__()

def is_followable(o):
    if o is None:
        return False
    elif hasattr(o, "__cembed__"):
        return True
    elif isinstance(o, int) or isinstance(o, float) or isinstance(o, str) or isinstance(o, list):
        return True
    elif hasattr(o, "__call__") or hasattr(o, "__getitem__"):
        return True
    else:
        return False

def is_embedable(o):
    if o is None:
        return False
    elif isinstance(o, int) or isinstance(o, float) or isinstance(o, str):
        return True
    elif isinstance(o, list):
        return all(is_embedable(x) for x in o)
    else:
        return hasattr(o, "__cembed__")