import os
import os.path
import sys
import glob
from .tokenizer import tokenize
from .pycp_parser import PYCPParser, CurlyParser
from .special import cdeps, cbuild, cdeps


def build(path=None, **kargs):
    q = []
    for k, v in kargs.items():
        v.label = k
        q.append(v)
    deps = []
    while q:
        dep = q.pop()
        if not dep in deps:
            deps.append(dep)
            q.extend(cdeps(dep))

    r = []
    for dep in deps:
        dep = cbuild(dep)
        if dep == None:
            continue
        for i in range(len(dep)):
            if i >= len(r):  # TODO
                r.append([])
            b = dep[i]
            if b != None:
                r[i].append(b)

    result = []
    for a in r:
        for b in a:
            if b not in result:
                result.append(b)
    result = "\n".join(result)
    if path != None:
        open(path + ".c", "w").write(result)  # join
    return result


def _convert_curly(r):
    b = []
    _curly_traverse(r, b, 0)
    t = []
    for i in range(len(b) - 1):
        t1 = b[i]
        t.append("    " * t1[0])
        t.append(t1[1])
        if b[i + 1][0] == t1[0] + 1:
            t.append(":\n")
        else:
            t.append("\n")
    t1 = b[-1]
    t.append(t1[0] * "    ")
    t.append(t1[1])
    t.append("\n")
    return "".join(t).replace("@{", "{")


def _curly_traverse(r, b, i):
    for a in r:
        if isinstance(a, str):
            b.append((i, a))
        else:
            b.append((i, a[0]))
            _curly_traverse(a[1], b, i + 1)


def process_file(file, output, cdef=True, curl=True, auto_import=True):
    code = open(file, "r").read()
    if cdef:
        tokens = tokenize(code)
        code = PYCPParser.parse(tokens, curl)
    if curl:
        tokens = tokenize(code)
        code = CurlyParser.parse(tokens)
        code = _convert_curly(code)
    with open(output, "w") as f:
        if auto_import:
            f.write("from pycpre import *\n")
        f.write(code)
