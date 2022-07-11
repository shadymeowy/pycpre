from .tokenizer import Symbol, PARANS, CPARANS, SEMICOLON, AT, TO
from .baseparser import BaseParser

template_strings = [
    'cfunction(locals(), globals(), {}, {}, {})',
    'cstruct(locals(), globals(), {})',
    'cinclude(locals(), globals(), {})',
    'cglobal(locals(), globals(), {}, {})',
    'creplace(locals(), globals(), {})',
    'ctypedef(locals(), globals(), {})',
    'cdefine(locals(), globals(), {})',
    'cmacro(locals(), globals(), {}, {})',
    'cfundef(locals(), globals(), {}, {})',
    '{} = cdef(locals(), globals(), {}, {}, {})',
]
template_strings_semicolon = template_strings.copy()
template_strings_semicolon[-1] += ';'


class PYCPParser(BaseParser):
    def _parse(self, semicolon=False):
        f = template_strings_semicolon if semicolon else template_strings
        r = []
        code = self.tokens.code
        while self.peeknm(None):
            if self.peekim(Symbol("cfunction")):
                start = self.last().start
                ret = self.readnwhile(PARANS[0])
                params = self.readrawparans(PARANS)
                body = self.readrawparans(CPARANS)
                stop = self.last().stop
                r.append((start, stop, f[0].format(
                    code[ret[0].start:ret[-1].stop].encode() if ret else b"",
                    code[params[0].start:params[-1].stop].encode() if params else b"",
                    code[body[0].start:body[-1].stop].encode() if body else b""
                )))
            elif self.peekim(Symbol("cstruct")):
                start = self.last().start
                body = self.readrawparans(CPARANS)
                stop = self.last().stop
                r.append((start, stop, f[1].format(
                    code[body[0].start:body[-1].stop].encode() if body else b""
                )))
            elif self.peekim(Symbol("cinclude")):
                start = self.last().start
                if self.peekm(CPARANS[0]):
                    body = self.readrawparans(CPARANS)
                else:
                    body = self.readrawparans(PARANS)
                stop = self.last().stop
                r.append((start, stop, f[2].format(
                    code[body[0].start:body[-1].stop].encode() if body else b""
                )))
            elif self.peekim(Symbol("cglobal")):
                start = self.last().start
                typ = self.readnwhile(CPARANS[0])
                body = self.readrawparans(CPARANS)
                stop = self.last().stop
                r.append((start, stop, f[3].format(
                    code[typ[0].start:typ[-1].stop].encode() if typ else b"",
                    code[body[0].start:body[-1].stop].encode() if body else b""
                )))
            elif self.peekim(Symbol("creplace")):
                start = self.last().start
                body = self.readrawparans(CPARANS)
                stop = self.last().stop
                r.append((start, stop, f[4].format(
                    code[body[0].start:body[-1].stop].encode() if body else b""
                )))
            elif self.peekim(Symbol("ctypedef")):
                start = self.last().start
                if self.peekm(CPARANS[0]):
                    body = self.readrawparans(CPARANS)
                else:
                    body = self.readrawparans(PARANS)
                stop = self.last().stop
                r.append((start, stop, f[5].format(
                    code[body[0].start:body[-1].stop].encode() if body else b""
                )))
            elif self.peekim(Symbol("cdefine")):
                start = self.last().start
                if self.peekm(CPARANS[0]):
                    body = self.readrawparans(CPARANS)
                else:
                    body = self.readrawparans(PARANS)
                stop = self.last().stop
                r.append((start, stop, f[6].format(
                    code[body[0].start:body[-1].stop].encode() if body else b""
                )))
            elif self.peekim(Symbol("cmacro")):
                start = self.last().start
                params = self.readrawparans(PARANS)
                body = self.readrawparans(CPARANS)
                stop = self.last().stop
                r.append((start, stop, f[7].format(
                    code[params[0].start:params[-1].stop].encode() if params else b"",
                    code[body[0].start:body[-1].stop].encode() if body else b""
                )))
            elif self.peekim(Symbol("cfundef")):
                start = self.last().start
                ret = self.readnwhile(PARANS[0])
                params = self.readrawparans(PARANS)
                stop = self.last().stop
                r.append((start, stop, f[8].format(
                    code[ret[0].start:ret[-1].stop].encode() if ret else b"",
                    code[params[0].start:params[-1].stop].encode() if params else b""
                )))
            elif self.peekim(Symbol("cdef")):
                start = self.last().start
                ret = self.readnwhile(PARANS[0])
                name, ret = ret[-1], ret[:-1]
                params = self.readrawparans(PARANS)
                if self.peekim(TO):
                    if len(ret) > 0:
                        raise Exception("cannot have multiple return types in cdef")
                    ret = self.readnwhile(CPARANS[0])
                body = self.readrawparans(CPARANS)
                stop = self.last().stop
                r.append((start, stop, f[9].format(
                    code[name.start:name.stop] if ret else b"",
                    code[ret[0].start:ret[-1].stop].encode() if ret else b"",
                    code[params[0].start:params[-1].stop].encode() if params else b"",
                    code[body[0].start:body[-1].stop].encode() if body else b""
                )))
            else:
                self.inc()
        b = []
        start = 0
        for s in r:
            b.append(code[start:s[0]])
            b.append(s[2])
            start = s[1]
        b.append(code[start:-1])
        return "".join(b)


class CurlyParser(BaseParser):
    def _parse(self):
        r = []
        self.tokens.append(SEMICOLON)
        self.ll += 1
        while self.peeknm(None):
            r.append(self.expr())
        return r

    def expr(self):
        r = []
        start = self.peek().start
        stop = None
        while True:
            if self.peekm(CPARANS[0]):
                self.inc()
                while self.peekinm(CPARANS[1]):
                    r.append(self.expr())
                self.peekim(SEMICOLON)
                return self.tokens.code[start:stop], r
            elif self.peekm(SEMICOLON):
                self.inc()
                self.readwhile(SEMICOLON)
                return self.tokens.code[start:stop]
            elif self.peekim(AT):
                if self.peekm(CPARANS[0]):
                    self.inc()
                else:
                    stop = self.read().stop
            else:
                stop = self.read().stop
