from .tokenizer import Symbol, PARANS, PARANS2, PARANS3, CPARANS, SEMICOLON, AT, TO, EQ, AS, STRING, SYMBOL
from .baseparser import BaseParser


class PYCPParser(BaseParser):
    def _start(self):
        self.start = self.last().start

    def _stop(self):
        self.stop = self.last().stop

    def _replace(self, value):
        self.replacements.append((self.start, self.stop, value))

    def _getn(self, tokens):
        if tokens:
            return self.tokens.code[tokens[0].start:tokens[-1].stop]
        else:
            return ''

    def _get(self, tokens):
        return repr(self._getn(tokens))

    def _parse(self):
        self.replacements = []
        code = self.tokens.code
        while self.peeknm(None):
            if self.peekim(Symbol("cfunction")):
                self._start()
                ret = self._get(self.readnwhile(PARANS[0]))
                params = self._get(self.readrawparans(PARANS))
                body = self._get(self.readrawparans(CPARANS))
                self._stop()
                self._replace('CFunction(locals(), globals(), "", {}, {}, {})'.format(ret, params, body))
            elif self.peekim(Symbol("cstruct")):
                self._start()
                name = self._getn(self.readnwhile(CPARANS[0]))
                body = self._get(self.readrawparans(CPARANS))
                self._stop()
                self._replace('{} = CStruct(locals(), globals(), {}, {});'.format(name, repr(name), body))
            elif self.peekim(Symbol("cinclude")):
                self._start()
                if self.peekm(PARANS3[0]):
                    header = repr("<{}>".format(self._getn(self.readrawparans(PARANS3))))
                elif self.peekm(STRING):
                    header = self._get((self.read(),))
                else:
                    raise Exception('Expected header name or string')
                if self.peekim(AS):
                    if self.peekm(SYMBOL):
                        name = self._getn((self.read(),))
                    else:
                        raise Exception('Expected a symbol for included header')
                else:
                    name = "_"
                self._stop()
                self._replace('{} = CInclude(locals(), globals(), {});'.format(name, header))
            elif self.peekim(Symbol("cglobal")):
                self._start()
                compound = self.readwhilef(lambda t: t != EQ and t != SEMICOLON)
                name = self._getn(compound[-1:])
                ret = self._get(compound[:-1])
                if self.peekim(SEMICOLON):
                    body = None
                elif self.peekim(EQ):
                    body = self._get(self.readnwhile(SEMICOLON))
                else:
                    raise Exception()
                self._stop()
                self._replace('{} = CGlobal(locals(), globals(), {}, {}, {});'.format(name, repr(name), typ, body))
            elif self.peekim(Symbol("ctypedef")):
                self._start()
                parans = CPARANS if self.peekm(CPARANS[0]) else PARANS
                body = self._get(self.readrawparans(parans))
                self._stop()
                self._replace('CTypedef(locals(), globals(), {})'.format(body))
            elif self.peekim(Symbol("cdefine")):
                self._start()
                parans = CPARANS if self.peekm(CPARANS[0]) else PARANS
                body = self._get(self.readrawparans(parans))
                self._stop()
                self._replace('CDefine(locals(), globals(), {})'.format(body))
            elif self.peekim(Symbol("cmacro")):
                self._start()
                name = self._getn(self.readnwhile(PARANS[0]))
                params = self._get(self.readrawparans(PARANS))
                body = self._get(self.readrawparans(CPARANS))
                self._stop()
                self._replace('{} = CMacro(locals(), globals(), {}, {}, {});'.format(name, repr(name), params, body))
            elif self.peekim(Symbol("cfundef")):
                self._start()
                ret = self._get(self.readnwhile(PARANS[0]))
                params = self._get(self.readrawparans(PARANS))
                self._stop()
                self._replace('CFunctionTypedef(locals(), globals(), {}, {})'.format(ret, params))
            elif self.peekim(Symbol("carraydef")):
                self._start()
                typ = self._get(self.readnwhile(PARANS2[0]))
                size = self._get(self.readrawparans(PARANS2))
                self._stop()
                self._replace('CArrayTypedef(locals(), globals(), {}, {})'.format(typ, size))
            elif self.peekim(Symbol("cdef")):
                self._start()
                compound = self.readnwhile(PARANS[0])
                name = self._getn(compound[-1:])
                ret = self._get(compound[:-1])
                params = self._get(self.readrawparans(PARANS))
                if self.peekim(TO):
                    if len(ret) > 0:
                        raise Exception("cannot have multiple return types in cdef")
                    ret = self.readnwhile(CPARANS[0])
                body = self._get(self.readrawparans(CPARANS))
                self._stop()
                self._replace('{} = CFunction(locals(), globals(), {}, {}, {}, {});'.format(
                    name, repr(name), ret, params, body))
            else:
                self.inc()
        b = []
        start = 0
        for s in self.replacements:
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
