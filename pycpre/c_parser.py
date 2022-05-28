from .baseparser import BaseParser
from .tokenizer import SYMBOL, DOT, PARANS, PARANS2
from .special import cembed, is_followable, is_embedable

MAGIC = "____PYCPRE_MAGIC____"


class CParser(BaseParser):
    def _parse(self, l, g):
        r = []
        code = self.tokens.code
        while self.peeknm(None):
            t = self.peek().value
            o = getattr(g["__builtins__"], t) if hasattr(g["__builtins__"], t) else None
            o = g[t] if t in g else o
            o = l[t] if t in l else o
            if is_followable(o):
                r.append(self.expr(o, l, g, code))
            else:
                if not o is None:
                    print(f"Warning: '{t}' exists in lexical scope but not followable: {o}")
                self.inc()

        fragments = []
        head = 0
        for start, stop, o in r:
            if is_embedable(o):
                fragments.append(code[head:start])
                fragments.append(cembed(o))
                head = stop
            else:
                print(f"Warning: '{code[start:stop]}' followed but is not embedable: {o}")
        fragments.append(code[head:-1])
        return "".join(fragments), [a[2] for a in r if hasattr(a[2], "__cembed__")]

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
