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
