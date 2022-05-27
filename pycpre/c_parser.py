from .baseparser import BaseParser
from .tokenizer import SYMBOL, DOT, PARANS, PARANS2
from .special import cembed

MAGIC = "____PYCPRE_MAGIC____"


class CParser(BaseParser):
    def _parse(self, l, g):
        r = []
        code = self.tokens.code
        while self.peeknm(None):
            t = self.peek().value
            if t in l:
                r.append(self.expr(l[t], l, g, code))
            elif t in g:
                r.append(self.expr(g[t], l, g, code))
            elif hasattr(g["__builtins__"], t):
                r.append(self.expr(getattr(g["__builtins__"], t), l, g, code))
            else:
                self.inc()
        b = []
        start = 0
        for s in r:
            b.append(code[start:s[0]])
            b.append(cembed(s[2]))
            start = s[1]
        b.append(code[start:-1])
        return "".join(b), [a[2] for a in r]

    def expr(self, curr, l, g, code):
        start = self.read().start
        while self.peeknm(None):
            if self.peekim(DOT):
                if self.peekm(SYMBOL):
                    t = self.read().value
                    if hasattr(curr, t):
                        curr = getattr(curr, t)
                    else:
                        self.i -= 2
                        break
                else:
                    self.i -= 1
                    break
            elif self.peekm(PARANS[0]):
                if hasattr(curr, "__call__"):
                    t = self.readrawparans(PARANS, include=True)
                    lc = dict(l)
                    lc[MAGIC] = curr
                    curr = eval(MAGIC + code[t[0].start:t[-1].stop], lc, g)
                else:
                    break
            elif self.peekm(PARANS2[0]):
                if hasattr(curr, "__getitem__"):
                    t = self.readrawparans(PARANS2, include=True)
                    lc = dict(l)
                    lc[MAGIC] = curr
                    curr = eval(MAGIC + code[t[0].start:t[-1].stop], lc, g)
                else:
                    break
            else:
                break
        return start, self.last().stop, curr
