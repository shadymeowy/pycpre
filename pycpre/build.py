from .tokenizer import tokenize
from .pycp_parser import PYCPParser
from .special import cdeps, cbuild, cdeps


def build(*args, path=None, format=False, format_args=["-i"], formatter=None, **kargs):
    q = []
    for k, v in kargs.items():
        v.label = k
        if v not in q:
            q.append(v)
        else:
            raise ValueError("Duplicate dependency: {}".format(k))
    for v in args:
        v.label = v.name
        if v not in q:
            q.append(v)
        else:
            raise ValueError("Duplicate dependency: {}".format(v.name))
    deps = []
    while q:
        dep = q.pop()
        if not dep in deps:
            deps.append(dep)
            q.extend(cdeps(dep))
    
    r = []
    for dep in deps:
        fragments = cbuild(dep)
        if fragments == None:
            continue
        for i in range(len(fragments)):
            if i >= len(r):  # TODO
                r.append([])
            b = fragments[i]
            if b != None:
                if isinstance(b, list) or isinstance(b, tuple):
                    for f in b:
                        if f != None:
                            r[i].append(f)
                else:
                    r[i].append(b)

    result = []
    for a in r:
        for b in reversed(a):
            if b not in result:
                result.append(b)
    result = "\n".join(result)
    if path != None:
        open(path, "w").write(result)  # join
    if format:
        import subprocess
        if formatter is None:
            formatter = "clang-format"
        subprocess.call(["clang-format", path, *format_args])
    return result


def process_file(file, output, cdef=True, curl=False, auto_import=True):
    code = open(file, "r").read()
    if cdef:
        tokens = tokenize(code)
        code = PYCPParser.parse(tokens)
    if curl:
        from .curly_parser import CurlyParser, convert_curly
        tokens = tokenize(code)
        code = CurlyParser.parse(tokens)
        code = convert_curly(code)
    with open(output, "w") as f:
        if auto_import:
            f.write("from pycpre import *\n")
        f.write(code)