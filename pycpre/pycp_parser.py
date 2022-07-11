from .tokenizer import Symbol, PARANS, CPARANS, SEMICOLON, AT
from .baseparser import BaseParser

template_strings = [
    'cdef(locals(), globals(), {}, {}, {})',
    'cstruct(locals(), globals(), {})',
    'cinclude(locals(), globals(), {})',
    'cglobal(locals(), globals(), {}, {})',
    'creplace(locals(), globals(), {})',
    'ctypedef(locals(), globals(), {})',
    'cdefine(locals(), globals(), {})',
    'cmacro(locals(), globals(), {}, {})',
    'cfundef(locals(), globals(), {}, {})',
]
template_strings_semicolon = list(map(lambda x: x + ";", template_strings))


class PYCPParser(BaseParser):
    def _parse(self, semicolon=False):
        f = template_strings_semicolon if semicolon else template_strings
        r = []
        code = self.tokens.code
        while self.peeknm(None):
            if self.peekim(Symbol("cdef")):
                start = self.last().start
                typ = self.readnwhile(PARANS[0])
                params = self.readrawparans(PARANS)
                body = self.readrawparans(CPARANS)
                stop = self.last().stop
                r.append((start, stop, f[0].format(
                    code[typ[0].start:typ[-1].stop].encode() if typ else b"",
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
                body = self.readnwhile(SEMICOLON)
                self.inc()
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
                body = self.readnwhile(SEMICOLON)
                self.inc()
                stop = self.last().stop
                r.append((start, stop, f[5].format(
                    code[body[0].start:body[-1].stop].encode() if body else b""
                )))
            elif self.peekim(Symbol("cdefine")):
                start = self.last().start
                body = self.readnwhile(SEMICOLON)
                self.inc()
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
                typ = self.readnwhile(PARANS[0])
                params = self.readrawparans(PARANS)
                stop = self.last().stop
                r.append((start, stop, f[8].format(
                    code[typ[0].start:typ[-1].stop].encode() if typ else b"",
                    code[params[0].start:params[-1].stop].encode() if params else b""
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
