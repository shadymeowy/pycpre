from .tokenizer import CPARANS, SEMICOLON, AT
from .baseparser import BaseParser

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


def convert_curly(r):
    b = []
    _curly_traverse(r, b, 0)
    t = []
    for i in range(len(b) - 1):
        t1 = b[i]
        t.append("    " * t1[0])
        t.append(t1[1])
        if b[i + 1][0] == t1[0] + 1:
            t.append(":\n")
        else:
            t.append("\n")
    t1 = b[-1]
    t.append(t1[0] * "    ")
    t.append(t1[1])
    t.append("\n")
    return "".join(t).replace("@{", "{")


def _curly_traverse(r, b, i):
    for a in r:
        if isinstance(a, str):
            b.append((i, a))
        else:
            b.append((i, a[0]))
            _curly_traverse(a[1], b, i + 1) 
