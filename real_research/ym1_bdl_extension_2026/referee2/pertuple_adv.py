#!/usr/bin/env python3
"""
Task 1c: the two NEW per-tuple inequalities of Lemma 3' (DERIVATION.md S7), adversarially, k = 0..8:
  (ME)  ||X_tau Omega|| <= 2^k J prod ||c_{M_i}||                         (operator-norm step)
  (CS)  sum_{M ni u} ||Pi_M X_tau Omega|| / |M| <= gamma(u) ||X_tau Omega||  (sector Cauchy-Schwarz)
        gamma(u) = gamma0 (u in p) ; gamma_S / max_j |M_j|  (u not in p, u in N)   [most stringent j]
tau = (M_1..M_k, p): one set per slot, one 4-site plaquette p = {0,1,2,3}, off-p sites 4..n-1.
Qutrits (q=3, sector vectors 2^|M|-dimensional) for n=7, qubits for n=10.
Adam over V_p (general complex, op-norm normalised) and the sector vectors; random set tuples.
"""
import itertools, math, sys, json
import numpy as np, torch
from toy import Toy, CD, opnorm, gam0, gamS

def run(n, q, ks, ntuples, steps, seed):
    rng = np.random.default_rng(seed)
    toy = Toy(n, q, [(0, 1, 2, 3)])
    P = {0, 1, 2, 3}
    res = {}
    for k in ks:
        bestCS, bestME = 0.0, 0.0
        for t in range(ntuples):
            # random tuple: each M_i meets p (else X=0); bias toward configurations that survive at depth k
            # STRUCTURED tuple that survives at depth k: R right-sets, L left-sets (each side pairwise
            # disjoint, every set meets p), off-p parts pairwise disjoint over all k sets.
            R = int(rng.integers(max(0, k - 4), min(4, k) + 1)); Lk = k - R
            offpool = list(rng.permutation(np.arange(4, n)))
            Ms = []
            for side in (R, Lk):
                if side == 0: continue
                ps = rng.permutation(4)[: int(rng.integers(side, 5))]
                assign = list(range(side)) + list(rng.integers(0, side, size=len(ps) - side))
                rng.shuffle(assign)
                groups = [set() for _ in range(side)]
                for site_, g_ in zip(ps, assign): groups[g_].add(int(site_))
                for gset in groups:
                    for _ in range(int(rng.integers(0, 3))):
                        if offpool: gset.add(int(offpool.pop()))
                    Ms.append(tuple(sorted(gset)))
            rng.shuffle(Ms)
            Ss = [toy.family_struct([M]) for M in Ms]
            g = torch.Generator().manual_seed(int(rng.integers(1 << 30)))
            pars = [torch.nn.Parameter(torch.randn(2, S["npar"], generator=g)) for S in Ss]
            Vp = torch.nn.Parameter(torch.randn(2, q ** 4, q ** 4, generator=g))
            opt = torch.optim.Adam(pars + [Vp], lr=0.05)
            N = set().union(*[set(M) for M in Ms]) if k else set()
            maxMj = max((len(M) for M in Ms), default=0)
            for it in range(steps):
                cp = [torch.complex(p[0], p[1]) for p in pars]
                with torch.no_grad():
                    Vc = torch.complex(Vp[0], Vp[1]); nrm = torch.linalg.matrix_norm(Vc, ord=2)
                    Vp.data /= nrm
                V = torch.complex(Vp[0], Vp[1]); J = 1.0
                v = toy.nested(Ss, cp, [V]) if k else toy.apply_V([V], torch.eye(toy.dim, dtype=CD)[:, :1])[:, 0]
                nv = torch.linalg.vector_norm(v)
                if float(nv) < 1e-12:
                    break
                sec = toy.sector_norms(v)
                masks = np.arange(1 << n); pcm = np.array([bin(m).count("1") for m in masks])
                terms = []
                for u in range(n):
                    w = torch.tensor(np.where(pcm > 0, ((masks >> u) & 1) / np.maximum(pcm, 1), 0.0))
                    lhs = w @ sec
                    if u in P:
                        gam = gam0(4)
                    elif u in N:
                        gam = gamS(4) / maxMj
                    else:
                        continue
                    terms.append(lhs / (gam * nv))
                rCS = torch.stack(terms).max()
                den = J * 2 ** k
                for c in cp:
                    den = den * torch.linalg.vector_norm(c)
                rME = nv / den
                if not (np.isfinite(float(rCS)) and np.isfinite(float(rME))):
                    break
                bestCS = max(bestCS, float(rCS)); bestME = max(bestME, float(rME) * float(torch.linalg.matrix_norm(V.detach(), ord=2)) ** 0)
                loss = -(torch.log(rCS) + 0.3 * torch.log(rME))
                loss.backward(); opt.step(); opt.zero_grad()
        res[k] = (bestCS, bestME)
        print(f"  n={n} q={q} k={k}: worst (CS) ratio {bestCS:.4f}   worst (ME) ratio {bestME:.4f}", flush=True)
    return res

if __name__ == "__main__":
    which = sys.argv[1]
    if which == "q3":
        r = run(7, 3, range(0, 9), ntuples=12, steps=120, seed=11)
    else:
        r = run(10, 2, range(0, 9), ntuples=25, steps=150, seed=12)
    json.dump({str(k): v for k, v in r.items()}, open(f"pertuple_{which}.json", "w"))
