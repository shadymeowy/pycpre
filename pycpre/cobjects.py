from .tokenizer import tokenize
from .c_parser import CParser
from .special import cembed, cbuild, cdeps


class CCode():
    def __init__(self, l, g, code):
        self.code = code
        self.locals = l
        self.globals = g

    def process(self):
        tokens = tokenize(self.code)
        return CParser.parse(tokens, self.locals, self.globals)


class CFunction():
    def __init__(self, l, g, ret, args, body):
        self.ret = CCode(l, g, ret)
        self.args = CCode(l, g, args)
        self.body = CCode(l, g, body)
        self.label = label()
        self.cache = None
        self.deps = []

    def __cbuild__(self):
        if self.cache == None:
            rett = self.ret.process()
            argst = self.args.process()
            bodyt = self.body.process()
            sig = "{} {}({})".format(rett[0], self.label, argst[0])
            fimp = "{} {{\n{}\n}}".format(sig, bodyt[0])
            self.cache = build_template(fdec=sig + ";", fimp=fimp)
            self.deps.extend(rett[1])
            self.deps.extend(argst[1])
            self.deps.extend(bodyt[1])
            self.deps = list(set(self.deps))
        return self.cache

    def __cembed__(self):
        return self.label

    def __cdeps__(self):
        self.__cbuild__()
        return self.deps


class CStruct():
    def __init__(self, l, g, body):
        self.body = CCode(l, g, body)
        self.label = label()
        self.cache = None
        self.deps = []

    def __cbuild__(self):
        if self.cache == None:
            bodyt = self.body.process()
            sdec = "struct tag_{0};\ntypedef struct tag_{0} {0};".format(
                self.label)
            simp = "struct tag_{}\n{{ {} }};".format(self.label, bodyt[0])
            self.cache = build_template(sdec=sdec, simp=simp)
            self.deps.extend(bodyt[1])
        return self.cache

    def __cembed__(self):
        return self.label

    def __cdeps__(self):
        self.__cbuild__()
        return self.deps


class CInclude():
    def __init__(self, value):
        self.value = value

    def __cembed__(self):
        raise Exception()

    def __cbuild__(self):
        return build_template(includes="#include {}".format(self.value))

    def __cdeps__(self):
        return []

    def __getattr__(self, value):
        return CRawDepend(value, [self])

    def __hasattr__(self, value):
        return True


class CGlobal():
    def __init__(self, l, g, ret, body):
        self.ret = CCode(l, g, ret)
        self.body = CCode(l, g, body)
        self.label = label()
        self.cache = None
        self.deps = []

    def __cbuild__(self):
        if self.cache == None:
            rett = self.ret.process()
            bodyt = self.body.process()
            self.cache = build_template(
                glbs="{} {} = {};".format(rett[0], self.label, bodyt[0]))
            self.deps.extend(rett[1])
            self.deps.extend(bodyt[1])
            self.deps = list(set(self.deps))
        return self.cache

    def __cembed__(self):
        return self.label

    def __cdeps__(self):
        self.__cbuild__()
        return self.deps


class CReplace():
    def __init__(self, l, g, body):
        self.body = CCode(l, g, body)
        self.cache = None
        self.deps = []

    def __cbuild__(self):
        if self.cache == None:
            bodyt = self.body.process()
            self.cache = bodyt[0]
            self.deps.extend(bodyt[1])
            self.deps = list(set(self.deps))
        return build_template()

    def __cembed__(self):
        self.__cbuild__()
        return self.cache

    def __cdeps__(self):
        self.__cbuild__()
        return self.deps


class CTypedef():
    def __init__(self, l, g, body):
        self.body = CCode(l, g, body)
        self.label = label()
        self.cache = None
        self.deps = []

    def __cbuild__(self):
        if self.cache == None:
            bodyt = self.body.process()
            self.cache = build_template(
                ftypedef="typedef {} {};".format(bodyt[0], self.label))
            self.deps.extend(bodyt[1])
            self.deps = list(set(self.deps))
        return self.cache

    def __cembed__(self):
        return self.label

    def __cdeps__(self):
        self.__cbuild__()
        return self.deps


class CDefine():
    def __init__(self, l, g, body):
        self.body = CCode(l, g, body)
        self.label = label()
        self.cache = None
        self.deps = []

    def __cbuild__(self):
        if self.cache == None:
            bodyt = self.body.process()
            self.cache = build_template(
                defs="#define {} {}".format(self.label, bodyt[0]))
            self.deps.extend(bodyt[1])
            self.deps = list(set(self.deps))
        return self.cache

    def __cembed__(self):
        return self.label

    def __cdeps__(self):
        self.__cbuild__()
        return self.deps


class CMacro():
    def __init__(self, l, g, args, body):
        self.args = CCode(l, g, args)
        self.body = CCode(l, g, body)
        self.label = label()
        self.cache = None
        self.deps = []

    def __cbuild__(self):
        if self.cache == None:
            argst = self.args.process()
            bodyt = self.body.process()
            self.cache = build_template(
                defs="#define {}({}) {}".format(self.label, argst[0], bodyt[0]))
            self.deps.extend(argst[1])
            self.deps.extend(bodyt[1])
            self.deps = list(set(self.deps))
        return self.cache

    def __cembed__(self):
        return self.label

    def __cdeps__(self):
        self.__cbuild__()
        return self.deps


class CRaw():
    def __init__(self, value):
        self.value = value

    def __cembed__(self):
        return self.value

    def __cbuild__(self):
        return build_template()

    def __cdeps__(self):
        return []


class CDummySpace():
    def __cembed__(self):
        raise Exception()

    def __cbuild__(self):
        return build_template()

    def __cdeps__(self):
        return []

    def __getattr__(self, value):
        return CRaw(value)

    def __hasattr__(self, value):
        return True


C = CDummySpace()


class CRawDepend():
    def __init__(self, value, deps):
        self.value = value
        self.deps = deps

    def __cembed__(self):
        return self.value

    def __cbuild__(self):
        return build_template()

    def __cdeps__(self):
        return self.deps


def cdef(l, g, r, a, b):
    return CFunction(l, g, r.decode(), a.decode(), b.decode())


def cstruct(l, g, b):
    return CStruct(l, g, b.decode())


def cinclude(l, g, b):
    return CInclude(b.decode())


def cglobal(l, g, r, b):
    return CGlobal(l, g, r.decode(), b.decode())


def creplace(l, g, b):
    return CReplace(l, g, b.decode())


def ctypedef(l, g, b):
    return CTypedef(l, g, b.decode())


def cdefine(l, g, b):
    return CDefine(l, g, b.decode())


def cmacro(l, g, a, b):
    return CMacro(l, g, a.decode(), b.decode())


label_count = -1


def label():
    global label_count
    label_count += 1
    return "label{}".format(label_count)


def build_template(defs=None, includes=None, sdec=None, ftypedef=None, simp=None, stypedef=None, fdec=None, glbs=None, fimp=None):
    return [defs, includes, sdec, ftypedef, simp, stypedef, fdec, glbs, fimp]