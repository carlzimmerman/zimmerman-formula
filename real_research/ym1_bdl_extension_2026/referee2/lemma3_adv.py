#!/usr/bin/env python3
"""
Task 1: adversarial test of Lemma 3' (DERIVATION.md S7, (E5)):
   ||C_new||_1 <= beta_k (D J/Delta) prod_i ||C_i||_1 ,   C_new(M) = (H0^M)^{-1} Pi_M ad_{C1}..ad_{Ck}(V) Omega
for k = 0..8 on 4-body toys where depth 7 and 8 are NONZERO.  Gradient ascent (Adam, torch autograd)
on the ratio over ALL coefficients c^i_M (k independent creation operators) and over the plaquette
operators V_p (general complex, normalised by operator norm), with random restarts.
Output: worst ratio per k per toy (ratio > 1 would be a FAILURE of the lemma).
"""
import itertools, math, sys, time, json
import numpy as np, torch
from toy import Toy, beta, CD, opnorm

def torus2d_links(L=2):
    # d=2 periodic L x L: links (y, dir) ; plaquettes = 4 links
    idx = {}
    for y in itertools.product(range(L), repeat=2):
        for i in range(2):
            idx[(y, i)] = len(idx)
    sh = lambda y, i: tuple((y[a] + (a == i)) % L for a in range(2))
    pl = []
    for y in itertools.product(range(L), repeat=2):
        pl.append((idx[(y, 0)], idx[(sh(y, 0), 1)], idx[(sh(y, 1), 0)], idx[(y, 1)]))
    return len(idx), pl

def run_toy(name, toy, sets, ks, restarts, steps, lr=0.05, same_C=False, seed=0, init_scale=None):
    S = toy.family_struct(sets)
    res = {}
    for k in ks:
        best = 0.0
        g = torch.Generator().manual_seed(seed + 97 * k)
        for r in range(restarts):
            nC = 1 if same_C else k
            # init: random dense or sparse (few sets) or singletons-on-p
            mode = r % 3
            pars = []
            for i in range(nC):
                re = torch.randn(S["npar"], generator=g); im = torch.randn(S["npar"], generator=g)
                if mode == 1:   # sparse
                    mask = (torch.rand(S["npar"], generator=g) < 0.05).double()
                    re, im = re * mask + 1e-3 * re, im * mask + 1e-3 * im
                if mode == 2:   # emphasise small sets
                    sz = torch.tensor([len(S["sets"][j]) for j, (o, l) in enumerate(S["offs"]) for _ in range(l)], dtype=torch.float64)
                    re, im = re * torch.exp(-1.5 * (sz - 1)), im * torch.exp(-1.5 * (sz - 1))
                pars.append(torch.nn.Parameter(torch.stack([re, im])))
            Vs = [torch.nn.Parameter(torch.randn(2, toy.q ** 4, toy.q ** 4, generator=g)) for _ in toy.plaqs]
            opt = torch.optim.Adam(pars + Vs, lr=lr)
            last = None
            for it in range(steps):
                cp = [torch.complex(p[0], p[1]) for p in pars]
                if same_C:
                    cp = cp * k
                Vl = [torch.complex(V[0], V[1]) for V in Vs]
                J = torch.stack([opnorm(V) for V in Vl]).max()
                v = toy.nested([S] * k, cp, Vl) if k > 0 else toy.apply_V(Vl, torch.eye(toy.dim, dtype=CD)[:, :1])[:, 0]
                lhs = toy.norm1_out(v)
                den = J
                for c in (cp[:1] if same_C else cp):
                    den = den * (Toy.norm1_C(S, c) ** (k if same_C else 1))
                obj = torch.log(lhs + 1e-300) - torch.log(den)
                ratio = float(torch.exp(obj)) / (beta(k) * toy.D)
                best = max(best, ratio)
                (-obj).backward()
                opt.step(); opt.zero_grad()
        res[k] = best
        print(f"  [{name}] k={k}: worst ratio = {best:.4e}   (beta_k={beta(k):.4g}, D={toy.D})", flush=True)
    return res

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "A"
    out = {}
    t0 = time.time()
    if which == "A":   # qubits, one plaquette + 4 off sites (D=1)
        toy = Toy(8, 2, [(0, 1, 2, 3)])
        sets = [M for r in range(1, 9) for M in itertools.combinations(range(8), r) if set(M) & {0, 1, 2, 3}]
        out["A_distinct"] = run_toy("A qubit n=8 1plaq distinct C", toy, sets, range(0, 9), restarts=6, steps=300)
        out["A_same"] = run_toy("A qubit n=8 1plaq same C", toy, sets, range(1, 9), restarts=6, steps=300, same_C=True)
    if which == "B":   # qubits, 2x2 torus d=2 (8 links, 4 plaquettes, D=2)
        n, pl = torus2d_links(2)
        toy = Toy(n, 2, pl)
        sets = [M for r in range(1, n + 1) for M in itertools.combinations(range(n), r)]
        out["B_distinct"] = run_toy("B qubit 2x2 torus distinct C", toy, sets, range(0, 9), restarts=6, steps=300)
    if which == "C":   # qutrits, two overlapping plaquettes (D=2)
        toy = Toy(6, 3, [(0, 1, 2, 3), (2, 3, 4, 5)])
        sets = [M for r in range(1, 7) for M in itertools.combinations(range(6), r)]
        out["C_distinct"] = run_toy("C qutrit n=6 2plaq distinct C", toy, sets, range(0, 9), restarts=4, steps=250)
    if which == "D":   # qubits, one plaquette + 8 off sites; sets = T u W, |W|<=1 (room for 8 distinct off sites)
        toy = Toy(12, 2, [(0, 1, 2, 3)])
        sets = [tuple(sorted(T + W)) for r in range(1, 5) for T in itertools.combinations(range(4), r)
                for w in range(0, 2) for W in itertools.combinations(range(4, 12), w)]
        out["D_distinct"] = run_toy("D qubit n=12 1plaq |W|<=1", toy, sets, [1, 2, 5, 6, 7, 8], restarts=3, steps=150)
    print("elapsed", time.time() - t0)
    json.dump({k: {str(kk): vv for kk, vv in v.items()} for k, v in out.items()}, open(f"lemma3_{which}.json", "w"), indent=1)
