from .tokenizer import tokenize
from .c_parser import CParser
from .special import cembed, cbuild, cdeps


class CObject():
    def __init__(self):
        self.label = label()
        self.cache = None
        self.deps = []

    def __cembed__(self):
        raise NotImplementedError()

    def __cbuild__(self):
        return build_template()

    def __cdeps__(self):
        self.__cbuild__()
        return self.deps


class CFragment:
    def __init__(self, l, g, code):
        self.code = code
        self.locals = l
        self.globals = g

    def process(self):
        tokens = tokenize(self.code)
        return CParser.parse(tokens, self.locals, self.globals)


class CFunction(CObject):
    def __init__(self, l, g, ret, args, body):
        self.ret = CFragment(l, g, ret)
        self.args = CFragment(l, g, args)
        self.body = CFragment(l, g, body)
        super().__init__()

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

        return self.cache


class CStruct(CObject):
    def __init__(self, l, g, body):
        self.body = CFragment(l, g, body)
        super().__init__()

    def __cbuild__(self):
        if self.cache == None:
            bodyt = self.body.process()
            sdec = "struct tag_{0};\ntypedef struct tag_{0} {0};".format(
                self.label)
            simp = "struct tag_{}\n{{ {} }};".format(self.label, bodyt[0])
            self.cache = build_template(sdec=sdec, simp=simp)
            self.deps.extend(bodyt[1])
        return self.cache


class CInclude(CObject):
    def __init__(self, value):
        self.value = value
        super().__init__()

    def __cbuild__(self):
        return build_template(includes="#include {}".format(self.value))

    def __getattr__(self, value):
        return CRawDepend(value, [self])

    def __hasattr__(self, value):
        return True


class CGlobal(CObject):
    def __init__(self, l, g, ret, body):
        self.ret = CFragment(l, g, ret)
        self.body = CFragment(l, g, body)
        super().__init__()

    def __cbuild__(self):
        if self.cache == None:
            rett = self.ret.process()
            bodyt = self.body.process()
            self.cache = build_template(
                glbs="{} {} = {};".format(rett[0], self.label, bodyt[0]))
            self.deps.extend(rett[1])
            self.deps.extend(bodyt[1])

        return self.cache


class CReplace(CObject):
    def __init__(self, l, g, body):
        self.body = CFragment(l, g, body)
        super().__init__()

    def __cbuild__(self):
        if self.cache == None:
            bodyt = self.body.process()
            self.cache = bodyt[0]
            self.deps.extend(bodyt[1])

        return build_template()

    def __cembed__(self):
        self.__cbuild__()
        return self.cache

    def __cdeps__(self):
        self.__cbuild__()
        return self.deps


class CTypedef(CObject):
    def __init__(self, l, g, body):
        self.body = CFragment(l, g, body)
        super().__init__()

    def __cbuild__(self):
        if self.cache == None:
            bodyt = self.body.process()
            self.cache = build_template(
                ftypedef="typedef {} {};".format(bodyt[0], self.label))
            self.deps.extend(bodyt[1])

        return self.cache


class CDefine(CObject):
    def __init__(self, l, g, body):
        self.body = CFragment(l, g, body)
        super().__init__()

    def __cbuild__(self):
        if self.cache == None:
            bodyt = self.body.process()
            self.cache = build_template(
                defs="#define {} {}".format(self.label, bodyt[0]))
            self.deps.extend(bodyt[1])

        return self.cache


class CMacro(CObject):
    def __init__(self, l, g, args, body):
        self.args = CFragment(l, g, args)
        self.body = CFragment(l, g, body)
        super().__init__()

    def __cbuild__(self):
        if self.cache == None:
            argst = self.args.process()
            bodyt = self.body.process()
            self.cache = build_template(
                defs="#define {}({}) {}".format(self.label, argst[0], bodyt[0].replace("\n", "\\\n")))
            self.deps.extend(argst[1])
            self.deps.extend(bodyt[1])

        return self.cache


class CFunctionTypedef(CObject):
    def __init__(self, l, g, ret, args):
        self.ret = CFragment(l, g, ret)
        self.args = CFragment(l, g, args)
        super().__init__()

    def __cbuild__(self):
        if self.cache == None:
            rett = self.ret.process()
            argst = self.args.process()
            self.cache = build_template(
                ftypedef="typedef {} (*{})({});".format(rett[0], self.label, argst[0]))
            self.deps.extend(rett[1])
            self.deps.extend(argst[1])

        return self.cache


class CRaw(CObject):
    def __init__(self, value):
        self.value = value
        super().__init__()

    def __cembed__(self):
        return self.value


class CDummySpace(CObject):
    def __getattr__(self, value):
        return CRaw(value)

    def __hasattr__(self, value):
        return True


C = CDummySpace()


class CRawDepend(CObject):
    def __init__(self, value, deps):
        self.value = value
        super().__init__()
        self.deps = deps

    def __cembed__(self):
        return self.value


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


def cfundef(l, g, r, a):
    return CFunctionTypedef(l, g, r.decode(), a.decode())


label_count = -1


def label():
    global label_count
    label_count += 1
    return "label{}".format(label_count)


def build_template(defs=None, includes=None, sdec=None, ftypedef=None, simp=None, stypedef=None, fdec=None, glbs=None, fimp=None):
    return [defs, includes, sdec, ftypedef, simp, stypedef, fdec, glbs, fimp]
