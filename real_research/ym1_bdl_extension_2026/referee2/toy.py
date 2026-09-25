#!/usr/bin/env python3
"""
Second-referee toy machinery (written from scratch; imports nothing from the lane).

Sites 0..n-1, local dimension q, vacuum = level 0.  All excitation energies = Delta = 1
(worst case for the resolvent: (H0^M)^{-1} = 1/|M| exactly on sector M).

Creation operator  C = sum_M A[c_M],  A[c_M] = |c_M><0_M| (x) 1,  c_M in K_M = (x)_{w in M} 0_w^perp,
represented by a parameter vector per allowed set M (length (q-1)^{|M|}).
Applied to a batch of vectors with gather / index_add (torch autograd friendly).

Nested commutator  ad_{C_1}...ad_{C_k}(V) Omega = sum_{T subset [k]} (-1)^{|T|} C_{[k]\\T} V C_T Omega,
computed by a subset DP (C's commute) in O(2^k) operator applications -> depth 8 on 2^12..2^16 dims.
"""
import itertools, math
from math import comb, factorial
import numpy as np
import torch

torch.set_default_dtype(torch.float64)
CD = torch.complex128


def gam0(s):
    return math.sqrt(sum(comb(s - 1, t - 1) / t ** 2 for t in range(1, s + 1)))


def gamS(s):
    return (s + 1) * math.sqrt(sum(comb(s, t) / (t + 1) ** 2 for t in range(0, s + 1)))


def beta(k, s=4):
    if k == 0:
        return gam0(s)
    return 2 ** k * (gam0(s) * s ** k + k * gamS(s) * s ** (k - 1))


class Toy:
    def __init__(self, n, q, plaqs):
        self.n, self.q, self.plaqs = n, q, [tuple(p) for p in plaqs]
        self.dim = q ** n
        st = np.array(list(itertools.product(range(q), repeat=n)), dtype=np.int64)
        self.st = st
        self.pw = q ** np.arange(n - 1, -1, -1)
        self.supp_mask = ((st != 0) * (1 << np.arange(n))).sum(1)       # bitmask of excited sites
        self.popc = np.array([bin(m).count("1") for m in self.supp_mask])
        self.D = max(sum(1 for p in self.plaqs if u in p) for u in range(n))
        # per-site membership (for ||.||_1 of an output vector): weight_u[i] = [u in supp(i)] / |supp(i)|
        W = np.zeros((n, self.dim))
        for u in range(n):
            sel = (self.supp_mask >> u) & 1
            W[u] = np.where(self.popc > 0, sel / np.maximum(self.popc, 1), 0.0)
        self.Wsite = torch.tensor(W)
        # sector id of each basis state (for sector norms of the output)
        self.sector_of = self.supp_mask
        self._cache = {}

    # ----- creation-operator structure for a family of sets
    def family_struct(self, sets):
        key = tuple(sorted(tuple(sorted(M)) for M in sets))
        if key in self._cache:
            return self._cache[key]
        rows, cols, pidx, offs = [], [], [], []
        off = 0
        for M in sets:
            M = sorted(M)
            nM = len(M)
            # source states: vacuum on M
            src = np.nonzero(np.all(self.st[:, M] == 0, axis=1))[0]
            confs = list(itertools.product(range(1, self.q), repeat=nM))
            for t, cf in enumerate(confs):
                add = sum(cf[j] * self.pw[M[j]] for j in range(nM))
                rows.append(src + add); cols.append(src); pidx.append(np.full(len(src), off + t))
            offs.append((off, len(confs)))
            off += len(confs)
        S = dict(rows=torch.tensor(np.concatenate(rows)), cols=torch.tensor(np.concatenate(cols)),
                 pidx=torch.tensor(np.concatenate(pidx)), offs=offs, npar=off,
                 sets=[frozenset(M) for M in sets])
        # site incidence for ||C||_1:  inc[u, j] = 1 if u in M_j
        inc = np.zeros((self.n, len(sets)))
        for j, M in enumerate(sets):
            for u in M:
                inc[u, j] = 1
        S["inc"] = torch.tensor(inc)
        self._cache[key] = S
        return S

    @staticmethod
    def apply_C(S, par, X):
        """X: (dim, B) complex; par: complex (npar,)"""
        vals = par[S["pidx"]]
        out = torch.zeros_like(X)
        out.index_add_(0, S["rows"], vals[:, None] * X[S["cols"]])
        return out

    @staticmethod
    def norm1_C(S, par):
        secn = torch.stack([torch.linalg.vector_norm(par[o:o + l]) for (o, l) in S["offs"]])
        return (S["inc"] @ secn).max()

    # ----- plaquette operators
    def apply_V(self, Vlist, X):
        """sum_p V_p X ; Vlist[i] is (q^4 x q^4) acting on plaqs[i] (ordered)"""
        n, q = self.n, self.q
        B = X.shape[1]
        out = torch.zeros_like(X)
        T = X.reshape([q] * n + [B])
        for Vp, p in zip(Vlist, self.plaqs):
            s = len(p)
            rest = [w for w in range(n) if w not in p]
            perm = list(p) + rest + [n]
            Tp = T.permute(perm).reshape(q ** s, -1)
            Yp = (Vp @ Tp).reshape([q] * n + [B])
            inv = np.argsort(perm).tolist()
            out = out + Yp.permute(inv).reshape(self.dim, B)
        return out

    def nested(self, Ss, pars, Vlist):
        """ad_{C_1}...ad_{C_k}(V) Omega  via the subset DP"""
        k = len(Ss)
        Om = torch.zeros(self.dim, 1, dtype=CD); Om[0, 0] = 1
        R = [None] * (1 << k)
        R[0] = Om
        for T in range(1, 1 << k):
            i = (T & -T).bit_length() - 1
            R[T] = self.apply_C(Ss[i], pars[i], R[T & (T - 1)])
        Rm = torch.cat(R, dim=1)                              # (dim, 2^k)
        Y = self.apply_V(Vlist, Rm)
        sign = torch.tensor([(-1) ** bin(T).count("1") for T in range(1 << k)], dtype=CD)
        F = Y * sign[None, :]
        for i in range(k):
            Fe, Fo = F[:, 0::2], F[:, 1::2]
            F = Fo + self.apply_C(Ss[i], pars[i], Fe)
        return F[:, 0]

    def norm1_out(self, v):
        """|| C_new ||_1 with c_M = Pi_M v / |M|  (all energies 1).  Needs sector 2-norms."""
        if self.q == 2:
            return (self.Wsite @ v.abs()).max()
        # sector 2-norms
        sec = torch.tensor(self.sector_of)
        nsec = 1 << self.n
        sq = torch.zeros(nsec).index_add_(0, sec, v.abs() ** 2)
        secnorm = torch.sqrt(sq + 1e-300)
        masks = np.arange(nsec)
        pc = np.array([bin(m).count("1") for m in masks])
        W = np.zeros((self.n, nsec))
        for u in range(self.n):
            W[u] = np.where(pc > 0, ((masks >> u) & 1) / np.maximum(pc, 1), 0.0)
        return (torch.tensor(W) @ secnorm).max()

    def sector_norms(self, v):
        sec = torch.tensor(self.sector_of)
        return torch.sqrt(torch.zeros(1 << self.n).index_add_(0, sec, v.abs() ** 2) + 1e-300)


def opnorm(V):
    return torch.linalg.matrix_norm(V, ord=2)


def dense_check(toy, Ss, pars, Vlist):
    """brute-force the nested commutator with dense matrices (small dims only)"""
    dim = toy.dim
    I = torch.eye(dim, dtype=CD)
    Cs = [toy.apply_C(S, p, I) for S, p in zip(Ss, pars)]
    V = toy.apply_V(Vlist, I)
    X = V
    for C in reversed(Cs):
        X = C @ X - X @ C
    Om = torch.zeros(dim, dtype=CD); Om[0] = 1
    return X @ Om
