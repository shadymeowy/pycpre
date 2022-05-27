def cembed(o):
    if isinstance(o, int) or isinstance(o, float):
        return str(o)
    elif isinstance(o, str):
        return "\"{}\"".format(o)
    else:
        return o.__cembed__()


def cdeps(o):
    if isinstance(o, int) or isinstance(o, float) or isinstance(o, str):
        return []
    else:
        return o.__cdeps__()


def cbuild(o):
    if isinstance(o, int) or isinstance(o, float) or isinstance(o, str):
        return None
    else:
        return o.__cbuild__()
