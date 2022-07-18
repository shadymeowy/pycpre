from .tokenizer import Symbol, PARANS, PARANS2, PARANS3, CPARANS, SEMICOLON, COMMA, TO, EQ, AS, STRING, SYMBOL, DOT
from .baseparser import BaseParser

STRUCT = Symbol("struct")
INCLUDE = Symbol("include")
CGLOBAL = Symbol("cglobal")
TYPEDEF = Symbol("typedef")
DEFINE = Symbol("define")
MACRO = Symbol("macro")
CDEF = Symbol("cdef")
FROM = Symbol("from")
IMPORT = Symbol("import")


class PYCPParser(BaseParser):
    def _start(self):
        self.start = self.last().start

    def _stop(self):
        self.stop = self.last().stop

    def _replace(self, value):
        self.replacements.append((self.start, self.stop, value))

    def _get_tokens(self, tokens):
        if tokens:
            return self.tokens.code[tokens[0].start:tokens[-1].stop]
        else:
            return ''

    def _get_generic(self):
        if self.peekm(PARANS2[0]):
            params = self._get_tokens(self.readrawparans(PARANS2))
            return 'generic(lambda {}: '.format(params)
        else:
            return '('

    def _get(self, tokens):
        return repr(self._get_tokens(tokens))

    def _get_header(self):
        if self.peekm(PARANS3[0]):
            return repr("<{}>".format(self._get_tokens(self.readrawparans(PARANS3)))), None
        elif self.peekm(STRING):
            return repr(self.read().value), None
        elif self.peekm(SYMBOL):
            t = []
            while True:
                t.append(self.read().value)
                if not self.peekim(DOT):
                    break
            if len(t) == 1:
                return repr('"{}.h"'.format(t[0])), t[0]
            else:
                return repr('"{}.h"'.format("/".join(t))), None
        else:
            raise Exception('Expected header name or string')

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
        if self.peekim(STRUCT):
            self._start()
            name = self._get_tokens(self.readwhilef(lambda t: t != CPARANS[0] and t != PARANS2[0]))
            generic = self._get_generic()
            body = self._get(self.readrawparans(CPARANS))
            self._stop()
            self._replace('{} = {}CStruct(locals(), globals(), {}, {}));'.format(name, generic, repr(name), body))
        elif self.peekim(INCLUDE):
            self._start()
            headers = []
            names = []
            while True:
                header, name = self._get_header()
                if self.peekim(AS):
                    if self.peekm(SYMBOL):
                        name = self.read().value
                    else:
                        raise Exception('Expected a symbol for included header')
                if not name:
                    name = "_"
                names.append(name)
                headers.append("CInclude({})".format(header))
                if not self.peekim(COMMA):
                    break
            self._stop()
            self._replace('{} = {};'.format(", ".join(names), ", ".join(headers)))
        elif self.peekim(CGLOBAL):
            self._start()
            compound = self.readwhilef(lambda t: t != EQ and t != SEMICOLON)
            if self.peekim(SEMICOLON):
                body = None
            elif self.peekim(EQ):
                body = self._get(self.readnwhile(SEMICOLON))
                self.inc()
            else:
                raise Exception()
            name = self._get_tokens(compound[-1:])
            ret = self._get(compound[:-1])
            self._stop()
            self._replace('{} = CGlobal(locals(), globals(), {}, {}, {});'.format(name, repr(name), ret, body))
        elif self.peekim(TYPEDEF):
            self._start()
            old_i = self.i
            definition = self.readnwhile(SEMICOLON)
            funptr = TO in definition
            self.i = old_i
            if funptr:
                name = self._get_tokens(self.readwhilef(lambda t: t != PARANS[0] and t != PARANS2[0]))
                generic = self._get_generic()
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
                name = self._get_tokens(compound[-1:])
                typ = self._get(compound[:-1])
                if self.peekim(SEMICOLON):
                    size = "''"
                else:
                    size = self._get(self.readnwhile(SEMICOLON))
                    self.inc()
                self._stop()
                self._replace('{} = CTypedef(locals(), globals(), {}, {}, {});'.format(
                    name, repr(name), typ, size))
        elif self.peekim(DEFINE):
            self._start()
            if self.peekm(SYMBOL):
                name = self.read().value
            else:
                raise Exception('Expected a symbol for defined macro')
            if self.peekm(CPARANS[0]):
                body = self._get(self.readrawparans(CPARANS))
            else:
                body = self._get(self.readnwhile(SEMICOLON))
                self.inc()
            self._stop()
            self._replace('{} = CDefine(locals(), globals(), {}, {});'.format(name, repr(name), body))
        elif self.peekim(MACRO):
            self._start()
            name = self._get_tokens(self.readnwhile(PARANS[0]))
            params = self._get(self.readrawparans(PARANS))
            body = self._get(self.readrawparans(CPARANS))
            self._stop()
            self._replace('{} = CMacro(locals(), globals(), {}, {}, {});'.format(name, repr(name), params, body))
        elif self.peekim(CDEF):
            self._start()
            name = self._get_tokens(self.readwhilef(lambda t: t != PARANS[0] and t != PARANS2[0]))
            generic = self._get_generic()
            params = self._get(self.readrawparans(PARANS))
            if self.peekim(TO):
                ret = self._get(self.readnwhile(CPARANS[0]))
            else:
                ret = repr("void")
            body = self._get(self.readrawparans(CPARANS))
            self._stop()
            self._replace('{} = {}CFunction(locals(), globals(), {}, {}, {}, {}));'.format(
                name, generic, repr(name), ret, params, body))
        elif self.peekim(FROM):
            self._start()
            old_i = self.i
            self.readwhilef(lambda t: t != IMPORT and t != INCLUDE)
            include = self.peekm(INCLUDE)
            self.i = old_i
            if not include:
                self.i -= 1
                return
            header, _ = self._get_header()
            self.peekirm(INCLUDE)
            names = []
            values = []
            while True:
                if self.peekm(SYMBOL):
                    value = self.read().value
                    name = value
                if self.peekim(AS):
                    if self.peekm(SYMBOL):
                        name = self.read().value
                    else:
                        raise Exception('Expected a symbol for included object')
                names.append(name)
                values.append(repr(value))
                if not self.peekim(COMMA):
                    break
            self._stop()
            self._replace("{}, = CInclude({}).get_attrs([{}]);".format(", ".join(names), header, ", ".join(values)))
        else:
            self.inc()