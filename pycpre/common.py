from .cobjects import *
from .generic import *
default_space = Namespace()
default_space.add = cmacro(locals(), globals(), b'a, b', b'((a)+(b))')
default_space.sub = cmacro(locals(), globals(), b'a, b', b'((a)-(b))')
default_space.mul = cmacro(locals(), globals(), b'a, b', b'((a)*(b))')
default_space.div = cmacro(locals(), globals(), b'a, b', b'((a)/(b))')
default_space.eq = cmacro(locals(), globals(), b'a, b', b'((a)==(b))')
default_space.ne = cmacro(locals(), globals(), b'a, b', b'((a)!=(b))')
default_space.lt = cmacro(locals(), globals(), b'a, b', b'((a)<(b))')
default_space.gt = cmacro(locals(), globals(), b'a, b', b'((a)>(b))')
default_space.le = cmacro(locals(), globals(), b'a, b', b'((a)<=(b))')
default_space.ge = cmacro(locals(), globals(), b'a, b', b'((a)>=(b))')
default_space.mod = cmacro(locals(), globals(), b'a, b', b'((a) % (b))')
default_space.lnot = cmacro(locals(), globals(), b'a', b'(!(a))')
default_space.neg = cmacro(locals(), globals(), b'a', b'(-(a))')
default_space.pos = cmacro(locals(), globals(), b'a', b'(+(a))')
default_space.lshift = cmacro(locals(), globals(), b'a, b', b'((a)<<(b))')
default_space.rshift = cmacro(locals(), globals(), b'a, b', b'((a)>>(b))')
default_space.land = cmacro(locals(), globals(), b'a, b', b'((a)&&(b))')
default_space.lor = cmacro(locals(), globals(), b'a, b', b'((a)||(b))')
default_space.band = cmacro(locals(), globals(), b'a, b', b'((a)&(b))')
default_space.bor = cmacro(locals(), globals(), b'a, b', b'((a)|(b))')
default_space.xor = cmacro(locals(), globals(), b'a, b', b'((a)^(b))')
default_space.bnot = cmacro(locals(), globals(), b'a', b'(~(a))')
default_space.iadd1 = cmacro(locals(), globals(), b'a', b'((a)++;')
default_space.isub1 = cmacro(locals(), globals(), b'a', b'((a)--;')
default_space.assign = cmacro(locals(), globals(), b'a, b', b'(a)=(b);')
default_space.iadd = cmacro(locals(), globals(), b'a, b', b'(a)+=(b);')
default_space.isub = cmacro(locals(), globals(), b'a, b', b'(a)-=(b);')
default_space.imul = cmacro(locals(), globals(), b'a, b', b'(a)*=(b);')
default_space.idiv = cmacro(locals(), globals(), b'a, b', b'(a)/=(b);')
default_space.imod = cmacro(locals(), globals(), b'a, b', b'(a)%=(b);')
default_space.isub = cmacro(locals(), globals(), b'a, b', b'(a)<<=(b);')
default_space.ilshift = cmacro(locals(), globals(), b'a, b', b'(a)>>=(b);')
default_space.irshift = cmacro(locals(), globals(), b'a, b', b'(a)/=(b);')
default_space.iband = cmacro(locals(), globals(), b'a, b', b'(a)&=(b);')
default_space.ibor = cmacro(locals(), globals(), b'a, b', b'(a)|=(b);')
default_space.ixor = cmacro(locals(), globals(), b'a, b', b'(a)^=(b);')
default_space.getindex = cmacro(locals(), globals(), b'a, b', b'((a)[(b)])')
default_space.setindex = cmacro(locals(), globals(), b'a, b, c', b'(a)[(b)]=(c);')
default_space.get = cmacro(locals(), globals(), b'a, b', b'((a).b)')
default_space.set = cmacro(locals(), globals(), b'a, b, c', b'(a).b=(c);')
default_space.getp = cmacro(locals(), globals(), b'a, b', b'((a)->b)')
default_space.setp = cmacro(locals(), globals(), b'a, b, c', b'(a)->b=(c);')
default_space.ref = cmacro(locals(), globals(), b'a', b'(&(a))')
default_space.deref = cmacro(locals(), globals(), b'a', b'(*(a))')
@generic_space
def default_type(S, name, format = None):
    S.update(default_space)
    if format:
        S.format = format
    return CRaw(name)
cchar = default_type("char", cdefine(locals(), globals(), b'"%c"'))
cuchar = default_type("unsigned char", cdefine(locals(), globals(), b'"%d"'))
cshort = default_type("short", cdefine(locals(), globals(), b'"%hi"'))
cushort = default_type("unsigned short", cdefine(locals(), globals(), b'"%hu"'))
cint = default_type("int", cdefine(locals(), globals(), b'"%d"'))
cuint = default_type("unsigned", cdefine(locals(), globals(), b'"%du"'))
clong = default_type("long", cdefine(locals(), globals(), b'"%ld"'))
culong = default_type("unsigned long", cdefine(locals(), globals(), b'"%lu"'))
cllong = default_type("long long", cdefine(locals(), globals(), b'"%lld"'))
cullong = default_type("unsigned long long", cdefine(locals(), globals(), b'"%llu"'))
cfloat = default_type("float", cdefine(locals(), globals(), b'"%f"'))
cdouble = default_type("double", cdefine(locals(), globals(), b'"%lf"'))
cvoid = default_type("void", cdefine(locals(), globals(), b'"%p"'))
C = CDummySpace()
def Pointer(T):
    return ctypedef(locals(), globals(), b'T*')
def Array(T, N):
    return carraydef(locals(), globals(), b'T', b'N')
def Include(path):
    return cinclude(locals(), globals(), b'path')
def Global(T, value):
    return cglobal(locals(), globals(), b'T', b'value')
def Typedef(T):
    return ctypedef(locals(), globals(), b'T')
def Define(value):
    return cdefine(locals(), globals(), b'value')
def FunctionPtr(R, T):
    return cfundef(locals(), globals(), b'R', b'tuple(T)')
