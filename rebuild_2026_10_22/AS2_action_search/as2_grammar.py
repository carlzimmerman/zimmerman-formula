#!/usr/bin/env python3
"""AS2 function grammar: bottom-up enumeration of f(y) with exact first and second derivatives on a fixed y grid.
Leaves y, u=y^2, 1, 2, 1/2. Unary neg inv sqrt log(1+.) log(1-.) exp. Binary + - * /. Distinct by (f, f', f'') to 1e-9.
Cap and max size from the command line; writes as2_grammar_cap<cap>.npz + .txt (no timing). One thread. kappa = 1/2 FITTED."""
import json, os, signal, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
YG = np.concatenate([np.geomspace(0.01, 0.97, 10), np.geomspace(1.3, 100.0, 6)])
NLOW = 10
NY = len(YG)
RNG = np.random.default_rng(20261102)
P1, P2, P3 = RNG.normal(size=NY), RNG.normal(size=NY), RNG.normal(size=NY)

def keyf(V, D, E):
    # hash on rounded projections with NaN as a sentinel; constant shifts stay distinct
    def sig(a):
        s = np.where(np.isfinite(a), np.sign(a) * np.log1p(np.abs(a)), 7.7)
        return s
    k1 = np.round((sig(V) * P1).sum(1) * 1e9)
    k2 = np.round((sig(D) * P2).sum(1) * 1e9)
    k3 = np.round((sig(E) * P3).sum(1) * 1e8)
    return k1 + 1e-3 * k2, k2 + 1e-3 * k3

def valid(V, D, E):
    fin = np.isfinite(V) & np.isfinite(D) & np.isfinite(E) & (np.abs(V) < 1e12) & (np.abs(D) < 1e12) & (np.abs(E) < 1e14)
    return fin[:, :NLOW].all(1)

def un(op, V, D, E):
    with np.errstate(all="ignore"):
        if op == "neg":
            return -V, -D, -E
        if op == "inv":
            return 1 / V, -D / V ** 2, (2 * D ** 2 / V - E) / V ** 2
        if op == "sqrt":
            s = np.sqrt(V); return s, D / (2 * s), E / (2 * s) - D ** 2 / (4 * s * V)
        if op == "log1p":
            w = 1 + V; return np.log(w), D / w, E / w - D ** 2 / w ** 2
        if op == "log1m":
            w = 1 - V; return np.log(w), -D / w, -E / w - D ** 2 / w ** 2
        if op == "exp":
            x = np.exp(V); return x, x * D, x * (E + D ** 2)
    raise ValueError(op)

def bi(op, A, B):
    Va, Da, Ea = A; Vb, Db, Eb = B
    with np.errstate(all="ignore"):
        if op == "+":
            return Va + Vb, Da + Db, Ea + Eb
        if op == "-":
            return Va - Vb, Da - Db, Ea - Eb
        if op == "*":
            return Va * Vb, Da * Vb + Va * Db, Ea * Vb + 2 * Da * Db + Va * Eb
        if op == "/":
            q = Va / Vb; dq = (Da - q * Db) / Vb
            return q, dq, (Ea - 2 * dq * Db - q * Eb) / Vb
    raise ValueError(op)

UN = ["neg", "inv", "sqrt", "log1p", "log1m", "exp"]
BI = ["+", "-", "*", "/"]

class G:
    def __init__(self, cap, maxsize):
        self.cap, self.maxsize = cap, maxsize
        self.V, self.D, self.E, self.expr, self.sz = [], [], [], [], []
        self.seen = set(); self.n = 0; self.raw = 0; self.by = {}; self.hitcap = None; self.stop = False
    def add(self, V, D, E, exprf, size):
        self.raw += len(V)
        ok = valid(V, D, E)
        if not ok.any():
            return
        idx = np.nonzero(ok)[0]
        V, D, E = V[idx], D[idx], E[idx]
        k1, k2 = keyf(V, D, E)
        keep = []
        for i, (a, b) in enumerate(zip(k1.tolist(), k2.tolist())):
            t = (a, b)
            if t not in self.seen:
                self.seen.add(t); keep.append(i)
        if not keep:
            return
        if self.n + len(keep) > self.cap:
            keep = keep[: self.cap - self.n]; self.hitcap = size
            if not keep:
                return
        kp = np.array(keep)
        self.V.append(V[kp]); self.D.append(D[kp]); self.E.append(E[kp])
        self.expr.extend(exprf(int(idx[i])) for i in keep)
        self.sz.extend([size] * len(keep)); self.n += len(keep)
        self.by[size] = self.by.get(size, 0) + len(keep)

    def run(self):
        y = YG; one = np.ones(NY); zero = np.zeros(NY)
        leaves = [("y", y, one, zero), ("u", y ** 2, 2 * y, 2 * one), ("1", one, zero, zero), ("2", 2 * one, zero, zero), ("h", 0.5 * one, zero, zero)]
        for n, v, d, e in leaves:
            self.add(v[None], d[None], e[None], lambda i, n=n: n, 1)
        self.blocks = {1: (np.vstack(self.V), np.vstack(self.D), np.vstack(self.E), list(self.expr))}
        for s in range(2, self.maxsize + 1):
            n0 = len(self.V); e0 = len(self.expr)
            if self.n >= self.cap:
                self.hitcap = self.hitcap or s; break
            for op in UN:
                if self.n >= self.cap or self.stop: break
                V, D, E, ex = self.blocks[s - 1]
                for c in range(0, len(V), 20000):
                    a, b, cc = un(op, V[c:c + 20000], D[c:c + 20000], E[c:c + 20000])
                    self.add(a, b, cc, lambda i, c=c, op=op, ex=ex: f"{op}({ex[c + i]})", s)
            for i in range(1, s - 1):
                j = s - 1 - i
                if self.n >= self.cap or self.stop: break
                for op in BI:
                    if op in "+*" and i > j:
                        continue
                    Va, Da, Ea, xa = self.blocks[i]
                    Vb, Db, Eb, xb = self.blocks[j]
                    for ca in range(0, len(Va), 200):
                        if self.n >= self.cap or self.stop: break
                        na = min(200, len(Va) - ca)
                        for cb in range(0, len(Vb), 5000):
                            nb = min(5000, len(Vb) - cb)
                            A = (np.repeat(Va[ca:ca + na], nb, 0), np.repeat(Da[ca:ca + na], nb, 0), np.repeat(Ea[ca:ca + na], nb, 0))
                            B = (np.tile(Vb[cb:cb + nb], (na, 1)), np.tile(Db[cb:cb + nb], (na, 1)), np.tile(Eb[cb:cb + nb], (na, 1)))
                            r = bi(op, A, B)
                            self.add(*r, (lambda t, ca=ca, cb=cb, nb=nb, op=op, xa=xa, xb=xb: f"({xa[ca + t // nb]}{op}{xb[cb + t % nb]})"), s)
                            if self.n >= self.cap or self.stop: break
            new = self.V[n0:]
            if new:
                self.blocks[s] = (np.vstack(new), np.vstack(self.D[n0:]), np.vstack(self.E[n0:]), self.expr[e0:])
            else:
                self.blocks[s] = (np.zeros((0, NY)), np.zeros((0, NY)), np.zeros((0, NY)), [])
            print(f"size {s}: distinct {self.by.get(s, 0)}, total {self.n}, raw tried {self.raw}", flush=True)
            if self.stop:
                break
        return self

def main():
    cap = int(sys.argv[1]); ms = int(sys.argv[2])
    g = G(cap, ms)
    signal.signal(signal.SIGTERM, lambda *a: setattr(g, "stop", True))
    g.run()
    if g.stop:
        print("stopped by SIGTERM; nothing written; rerun restarts this deterministic step"); sys.exit(3)
    out = os.path.join(HERE, f"as2_grammar_cap{cap}.npz")
    np.savez(out, y=YG, V=np.vstack(g.V), D=np.vstack(g.D), E=np.vstack(g.E), sz=np.array(g.sz, np.int8), expr=np.array(g.expr, dtype=object))
    meta = dict(cap=cap, maxsize=ms, distinct=g.n, raw_tried=g.raw, by_size={str(k): v for k, v in g.by.items()}, cap_hit_at_size=g.hitcap)
    json.dump(meta, open(out.replace(".npz", ".json"), "w"), indent=1, sort_keys=True)
    print(meta)

if __name__ == "__main__":
    main()
