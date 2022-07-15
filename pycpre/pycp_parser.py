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

    def _getg(self):
        if self.peekm(PARANS2[0]):
            params = self._getn(self.readrawparans(PARANS2))
            return 'generic(lambda {}: '.format(params)
        else:
            return '('

    def _get(self, tokens):
        return repr(self._getn(tokens))

    def _parse(self):
        self.replacements = []
        code = self.tokens.code
        while self.peeknm(None):
            self._parse_expr()
        b = []
        start = 0
        for s in self.replacements:
            b.append(code[start:s[0]])
            b.append(s[2])
            start = s[1]
        b.append(code[start:-1])
        return "".join(b)

    def _parse_expr(self):
        if self.peekim(Symbol("struct")):
            self._start()
            name = self._getn(self.readwhilef(lambda t: t != CPARANS[0] and t != PARANS2[0]))
            generic = self._getg()
            body = self._get(self.readrawparans(CPARANS))
            self._stop()
            self._replace('{} = {}CStruct(locals(), globals(), {}, {}));'.format(name, generic, repr(name), body))
        elif self.peekim(Symbol("include")):
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
            if self.peekim(SEMICOLON):
                body = None
            elif self.peekim(EQ):
                body = self._get(self.readnwhile(SEMICOLON))
                self.inc()
            else:
                raise Exception()
            name = self._getn(compound[-1:])
            ret = self._get(compound[:-1])
            self._stop()
            self._replace('{} = CGlobal(locals(), globals(), {}, {}, {});'.format(name, repr(name), ret, body))
        elif self.peekim(Symbol("typedef")):
            self._start()
            old_i = self.i
            definition = self.readnwhile(SEMICOLON)
            funptr = TO in definition
            self.i = old_i
            if funptr:
                name = self._getn(self.readwhilef(lambda t: t != PARANS[0] and t != PARANS2[0]))
                generic = self._getg()
                params = self._get(self.readrawparans(PARANS))
                if not self.peekim(TO):
                    raise Exception("Invalid function pointer definition")
                ret = self._get(self.readnwhile(SEMICOLON))
                self.inc()
                self._stop()
                self._replace('{} = {}CFunctionTypedef(locals(), globals(), {}, {}, {}));'.format(
                    name, generic, repr(name), ret, params))
            else:
                compound = self.readwhilef(lambda t: t != PARANS2[0] and t != SEMICOLON)
                name = self._getn(compound[-1:])
                typ = self._get(compound[:-1])
                if self.peekim(SEMICOLON):
                    size = "''"
                else:
                    size = self._get(self.readnwhile(SEMICOLON))
                    self.inc()
                self._stop()
                self._replace('{} = CTypedef(locals(), globals(), {}, {}, {});'.format(
                    name, repr(name), typ, size))
        elif self.peekim(Symbol("define")):
            self._start()
            if self.peekm(SYMBOL):
                name = self._getn((self.read(),))
            else:
                raise Exception('Expected a symbol for defined macro')
            if self.peekm(CPARANS[0]):
                body = self._get(self.readrawparans(CPARANS))
            else:
                body = self._get(self.readnwhile(SEMICOLON))
                self.inc()
            self._stop()
            self._replace('{} = CDefine(locals(), globals(), {}, {});'.format(name, repr(name), body))
        elif self.peekim(Symbol("macro")):
            self._start()
            name = self._getn(self.readnwhile(PARANS[0]))
            params = self._get(self.readrawparans(PARANS))
            body = self._get(self.readrawparans(CPARANS))
            self._stop()
            self._replace('{} = CMacro(locals(), globals(), {}, {}, {});'.format(name, repr(name), params, body))
        elif self.peekim(Symbol("cdef")):
            self._start()
            name = self._getn(self.readwhilef(lambda t: t != PARANS[0] and t != PARANS2[0]))
            generic = self._getg()
            params = self._get(self.readrawparans(PARANS))
            if self.peekim(TO):
                ret = self._get(self.readnwhile(CPARANS[0]))
            else:
                ret = repr("void")
            body = self._get(self.readrawparans(CPARANS))
            self._stop()
            self._replace('{} = {}CFunction(locals(), globals(), {}, {}, {}, {}));'.format(
                name, generic, repr(name), ret, params, body))
        else:
            self.inc()
