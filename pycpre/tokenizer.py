class Tokenizer():
    def __init__(self):
        self.ops = "+-*\#$!^%&/=?@:~<>"
        self.specials = ".,;()[]{}"
        self.whitespaces = "\n\t\r "
        self.quotes = "\"'`"
        self.digits = "0123456789"
        self.comment = "#"

    def tokenize(self, ss):
        ops = self.ops
        specials = self.specials
        whitespaces = self.whitespaces
        quotes = self.quotes
        digits = self.digits
        comment = self.comment
        lc = len(comment) == 2
        delim = self.ops + self.specials + self.whitespaces + self.quotes
        ss += "\n"
        r = []
        i = 0
        ll = len(ss)
        while i < ll:
            if ss[i] in whitespaces:
                i += 1
            elif lc and i + 1 < ll and ss[i] == comment[0] and ss[i + 1] == comment[1]:
                while ss[i] != "\n":
                    i += 1
                i += 1
            elif not lc and ss[i] == comment:
                while ss[i] != "\n":
                    i += 1
                i += 1
            elif ss[i] in ops:
                ti = i
                b = []
                while ss[i] in ops:
                    b.append(ss[i])
                    i += 1
                r.append(Operator("".join(b), ti, i))
            elif ss[i] in specials:
                r.append(Special(ss[i], i, i + 1))
                i += 1
            elif ss[i] in quotes:
                ti = i
                q = ss[i]
                i += 1
                b = [q]
                while ss[i] != q:
                    if ss[i] == "\\":
                        if ss[i + 1] == q:
                            i += 1
                        elif ss[i + 1] == "\\":
                            b.append("\\")
                            i += 2
                            continue
                    b.append(ss[i])
                    i += 1
                i += 1
                b.append(q)
                r.append(String("".join(b), ti, i))
            elif ss[i] in digits:
                ti = i
                b = []
                while not ss[i] in delim or ss[i] == ".":
                    b.append(ss[i])
                    i += 1
                r.append(Number("".join(b), ti, i))
            else:
                ti = i
                b = []
                while not ss[i] in delim:
                    b.append(ss[i])
                    i += 1
                r.append(Symbol("".join(b), ti, i))
        rt = Tokens()
        rt.tokens = r
        rt.code = ss
        return rt


class Token():
    __slots__ = "value", "start", "stop", "typenum", "typename"

    def __init__(self, value=None, start=-1, stop=-1):
        self.value = value
        self.start = start
        self.stop = stop
        self.init_type()

    def init_type(self):
        raise NotImplementedError()

    def __repr__(self):
        if not (self.start < 0 and self.stop < 0):
            if self.value == None:
                return "{}()".format(self.typename)
            else:
                return "{}({})".format(self.typename, repr(self.value))
        else:
            return "{}({}, start={}, stop={})".format(self.typename, repr(self.value), self.start, self.stop)

    def __eq__(self, other):
        return isinstance(other, Token) and (self.typenum == other.typenum) and ((self.value == other.value) or (self.value == None) or (other.value == None))

    def untokenize(self):
        return self.value

    __str__ = untokenize

    def __hash__(self):
        return hash(self.value)


class Symbol(Token):
    def init_type(self):
        self.typename = "Symbol"
        self.typenum = 0


class Number(Token):
    def init_type(self):
        self.typename = "Number"
        self.typenum = 1


class String(Token):
    def init_type(self):
        self.typename = "String"
        self.typenum = 2


class Special(Token):
    def init_type(self):
        self.typename = "Special"
        self.typenum = 3


class Operator(Token):
    def init_type(self):
        self.typename = "Operator"
        self.typenum = 4


class Tokens():
    def __str__(self):
        return "Tokens({})".format(str(self.tokens))

    def __repr__(self):
        return "Tokens({})".format(str(self.tokens))

    def copy(self):
        return Tokens(self.tokens.copy())

    def append(self, item):
        self.tokens.append(item)

    def extend(self, b):
        self.tokens.extend(b.tokens)

    def __getitem__(self, i):
        return self.tokens[i]

    def __len__(self):
        return len(self.tokens)

    def __iter__(self):
        return iter(self.tokens)

    @staticmethod
    def join(*args):
        r = Tokens()
        for arg in args:
            r.extend(arg)
        return r


SYMBOL = Symbol()
NUMBER = Number()
STRING = String()
SPECIAL = Special()
OP = Operator()
PARANS = Special("("), Special(")")
CPARANS = Special("{"), Special("}")
PARANS2 = Special("["), Special("]")
PARANS3 = Operator("<"), Operator(">")
SEMICOLON = Special(";")
DOT = Special(".")
COMMA = Special(",")
AT = Operator("@")
TO = Operator("->")
EQ = Operator("=")

__tokenizer = Tokenizer()


def tokenize(s):
    return __tokenizer.tokenize(s)
