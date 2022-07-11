def cembed(o):
    if isinstance(o, bool):
        return str(int(o))
    elif isinstance(o, int) or isinstance(o, float):
        return str(o)
    elif isinstance(o, str):
        return "\"{}\"".format(repr(o)[1:-1])
    elif isinstance(o, bytes):
        return "\"{}\"".format(repr(o)[2:-1])
    elif isinstance(o, bytearray):
        return "{{{}}}".format(", ".join(["0x{:02x}".format(x) for x in o]))
    elif isinstance(o, list):
        return "{{{}}}".format(", ".join(cembed(x) for x in o))
    elif isinstance(o, tuple):
        return ", ".join(cembed(x) for x in o)
    else:
        return o.__cembed__()


def cdeps(o):
    if (isinstance(o, int)
        or isinstance(o, float)
        or isinstance(o, str)
        or isinstance(o, bytes)
        or isinstance(o, bytearray)
            or isinstance(o, bool)):
        return []
    elif isinstance(o, list) or isinstance(o, tuple):
        r = []
        for x in o:
            r.extend(cdeps(x))
        return r
    else:
        return o.__cdeps__()


def cbuild(o):
    if (isinstance(o, int)
        or isinstance(o, float)
        or isinstance(o, str)
        or isinstance(o, bytes)
        or isinstance(o, bytearray)
            or isinstance(o, bool)):
        return build_template()
    elif isinstance(o, list) or isinstance(o, tuple):
        return list(zip(*(cbuild(x) for x in o)))
    else:
        return o.__cbuild__()


def is_followable(o):
    if o is None:
        return False
    elif hasattr(o, "__cembed__"):
        return True
    elif (isinstance(o, int)
          or isinstance(o, float)
          or isinstance(o, str)
          or isinstance(o, bytes)
          or isinstance(o, bytearray)
          or isinstance(o, bool)):
        return True
    elif hasattr(o, "__call__") or hasattr(o, "__getitem__") or hasattr(o, "__getattr__") or hasattr(o, "__getattribute__"):
        return True
    else:
        return False


def is_embedable(o):
    if o is None:
        return False
    elif (isinstance(o, int)
          or isinstance(o, float)
          or isinstance(o, str)
          or isinstance(o, bytes)
          or isinstance(o, bytearray)
          or isinstance(o, bool)):
        return True
    elif isinstance(o, list) or isinstance(o, tuple):
        return all(is_embedable(x) for x in o)
    else:
        return hasattr(o, "__cembed__")


def build_template(defs=None, includes=None, sdec=None, ftypedef=None, simp=None, stypedef=None, fdec=None, glbs=None, fimp=None):
    return [defs, includes, sdec, ftypedef, simp, stypedef, fdec, glbs, fimp]
