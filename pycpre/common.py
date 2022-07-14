from .cobjects import *
from .generic import *
class DefaultType(CRaw):
    def __init__(self, name, format = None):
        super().__init__(name)
        if format:
            self.format = format
    add = CMacro(locals(), globals(), 'add', 'a, b', '((a)+(b))')
    sub = CMacro(locals(), globals(), 'sub', 'a, b', '((a)-(b))')
    mul = CMacro(locals(), globals(), 'mul', 'a, b', '((a)*(b))')
    div = CMacro(locals(), globals(), 'div', 'a, b', '((a)/(b))')
    eq = CMacro(locals(), globals(), 'eq', 'a, b', '((a)==(b))')
    ne = CMacro(locals(), globals(), 'ne', 'a, b', '((a)!=(b))')
    lt = CMacro(locals(), globals(), 'lt', 'a, b', '((a)<(b))')
    gt = CMacro(locals(), globals(), 'gt', 'a, b', '((a)>(b))')
    le = CMacro(locals(), globals(), 'le', 'a, b', '((a)<=(b))')
    ge = CMacro(locals(), globals(), 'ge', 'a, b', '((a)>=(b))')
    mod = CMacro(locals(), globals(), 'mod', 'a, b', '((a) % (b))')
    lnot = CMacro(locals(), globals(), 'lnot', 'a', '(!(a))')
    neg = CMacro(locals(), globals(), 'neg', 'a', '(-(a))')
    pos = CMacro(locals(), globals(), 'pos', 'a', '(+(a))')
    lshift = CMacro(locals(), globals(), 'lshift', 'a, b', '((a)<<(b))')
    rshift = CMacro(locals(), globals(), 'rshift', 'a, b', '((a)>>(b))')
    land = CMacro(locals(), globals(), 'land', 'a, b', '((a)&&(b))')
    lor = CMacro(locals(), globals(), 'lor', 'a, b', '((a)||(b))')
    band = CMacro(locals(), globals(), 'band', 'a, b', '((a)&(b))')
    bor = CMacro(locals(), globals(), 'bor', 'a, b', '((a)|(b))')
    xor = CMacro(locals(), globals(), 'xor', 'a, b', '((a)^(b))')
    bnot = CMacro(locals(), globals(), 'bnot', 'a', '(~(a))')
    iadd1 = CMacro(locals(), globals(), 'iadd1', 'a', '((a)++)')
    isub1 = CMacro(locals(), globals(), 'isub1', 'a', '((a)--)')
    assign = CMacro(locals(), globals(), 'assign', 'a, b', '(a)=(b);')
    iadd = CMacro(locals(), globals(), 'iadd', 'a, b', '(a)+=(b);')
    isub = CMacro(locals(), globals(), 'isub', 'a, b', '(a)-=(b);')
    imul = CMacro(locals(), globals(), 'imul', 'a, b', '(a)*=(b);')
    idiv = CMacro(locals(), globals(), 'idiv', 'a, b', '(a)/=(b);')
    imod = CMacro(locals(), globals(), 'imod', 'a, b', '(a)%=(b);')
    isub = CMacro(locals(), globals(), 'isub', 'a, b', '(a)<<=(b);')
    ilshift = CMacro(locals(), globals(), 'ilshift', 'a, b', '(a)>>=(b);')
    irshift = CMacro(locals(), globals(), 'irshift', 'a, b', '(a)/=(b);')
    iband = CMacro(locals(), globals(), 'iband', 'a, b', '(a)&=(b);')
    ibor = CMacro(locals(), globals(), 'ibor', 'a, b', '(a)|=(b);')
    ixor = CMacro(locals(), globals(), 'ixor', 'a, b', '(a)^=(b);')
    getindex = CMacro(locals(), globals(), 'getindex', 'a, b', '((a)[(b)])')
    setindex = CMacro(locals(), globals(), 'setindex', 'a, b, c', '(a)[(b)]=(c);')
    get = CMacro(locals(), globals(), 'get', 'a, b', '((a).b)')
    set = CMacro(locals(), globals(), 'set', 'a, b, c', '(a).b=(c);')
    getp = CMacro(locals(), globals(), 'getp', 'a, b', '((a)->b)')
    setp = CMacro(locals(), globals(), 'setp', 'a, b, c', '(a)->b=(c);')
    ref = CMacro(locals(), globals(), 'ref', 'a', '(&(a))')
    deref = CMacro(locals(), globals(), 'deref', 'a', '(*(a))')
cchar = DefaultType("char", CDefine(locals(), globals(), '"%c"'))
cuchar = DefaultType("unsigned char", CDefine(locals(), globals(), '"%d"'))
cshort = DefaultType("short", CDefine(locals(), globals(), '"%hi"'))
cushort = DefaultType("unsigned short", CDefine(locals(), globals(), '"%hu"'))
cint = DefaultType("int", CDefine(locals(), globals(), '"%d"'))
cuint = DefaultType("unsigned", CDefine(locals(), globals(), '"%du"'))
clong = DefaultType("long", CDefine(locals(), globals(), '"%ld"'))
culong = DefaultType("unsigned long", CDefine(locals(), globals(), '"%lu"'))
cllong = DefaultType("long long", CDefine(locals(), globals(), '"%lld"'))
cullong = DefaultType("unsigned long long", CDefine(locals(), globals(), '"%llu"'))
cfloat = DefaultType("float", CDefine(locals(), globals(), '"%f"'))
cdouble = DefaultType("double", CDefine(locals(), globals(), '"%lf"'))
cvoid = DefaultType("void", CDefine(locals(), globals(), '"%p"'))
C = CDummySpace()
@generic
def Pointer(T):
    return CTypedef(locals(), globals(), 'T*')
@generic
def Array(T, N):
    return CArrayTypedef(locals(), globals(), 'T', 'N')
@generic
def Include(path):
    return CInclude(locals(), globals(), 'path')
@generic
def Global(T, value):
    r = CGlobal(locals(), globals(), 'r', 'T', 'value')
    return r
@generic
def Typedef(T):
    return CTypedef(locals(), globals(), 'T')
@generic
def Define(value):
    return CDefine(locals(), globals(), 'value')
@generic
def FunctionPtr(R, T):
    return CFunctionTypedef(locals(), globals(), 'R', 'tuple(T)')
