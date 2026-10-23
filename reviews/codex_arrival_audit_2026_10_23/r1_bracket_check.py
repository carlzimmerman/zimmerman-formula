#!/usr/bin/env python3
"""Codex arrival audit, Part A: is the DSF-21 / A33 constraint set first class?

Independent of Codex's checks.py (not read).  The Hamiltonian is A54 report section 1.3, with the magnetic
term (gamma/4) sqrt(h) F^2 restored from A68's frozen action:

  H_perp = (sqrt h/4K)(2 Lambda - R3) + (4K/sqrt h)[pi_ij pi^ij - c_b pi^2] + |pi_P|^2/(2 sqrt h eta)
         + sqrt h [D.P + (gamma/2)(D.P)^2 + W(u)] + (gamma/4) sqrt h F_ij F^ij + eps
  H_i    = -2 D_j pi^j_i + pi_P^k D_i P_k - D_k(pi_P^k P_i)

Lattice: periodic in x on [0, 2 pi), all fields depend on x only, unit transverse area, central differences.
Canonical pairs (h_a, p_a): p = pi^ii on the diagonal, p = 2 pi^ij off it; (P_i, pi_P^i).  {q_x, p_y} = delta_xy/dx.
eps = dust at rest (Brown-Kuchar, grad T = 0): a non-negative density commuting with every variable used here.

Checks A1-A5 (lattice + sympy) and A6 (sympy linear Dirac algorithm, Minkowski scalar sector) are frozen in
FROZEN_CRITERIA.md (+ AMENDMENT A1).  --mutate deletes the clock term everywhere (A1 must then FAIL).
"""
import json
import sys

import numpy as np
import sympy as sp

MUTATE = "--mutate" in sys.argv
OUT = "r1_results_MUTATE.json" if MUTATE else "r1_results.json"

K, ETA, GAMMA, A0 = 1.0, 1.0, 0.3, 1.0
IDX = [(0, 0), (1, 1), (2, 2), (0, 1), (0, 2), (1, 2)]


# ----------------------------------------------------------------------------- lattice Hamiltonian
class Lattice:
    def __init__(self, n, beta, lam, clock=True, eps=None):
        self.n, self.dx = n, 2 * np.pi / n
        self.x = self.dx * np.arange(n)
        self.beta, self.lam, self.clock = beta, lam, clock
        self.cb = (1 + beta) / (2 + 3 * beta)
        self.eps = np.zeros(n) if eps is None else eps

    def D(self, f):
        return (np.roll(f, -1, axis=-1) - np.roll(f, 1, axis=-1)) / (2 * self.dx)

    def D2(self, f):
        return (np.roll(f, -1, axis=-1) - 2 * f + np.roll(f, 1, axis=-1)) / self.dx ** 2

    @staticmethod
    def sym(v6, scale_off=1.0):
        m = np.zeros(v6.shape[1:] + (3, 3))
        for a, (i, j) in enumerate(IDX):
            m[..., i, j] = v6[a] * (1.0 if i == j else scale_off)
            m[..., j, i] = m[..., i, j]
        return m

    def ricci_scalar(self, h, h1, h2):
        """R3 for a metric depending on x only, from h and its first/second x-derivatives (exact formula)."""
        n = h.shape[0]
        hi = np.linalg.inv(h)
        dh = np.zeros((n, 3, 3, 3))      # dh[:, k, i, j] = d_k h_ij
        dh[:, 0] = h1
        ddh = np.zeros((n, 3, 3, 3))     # d_x d_k h_ij (only k = 0 non-zero)
        ddh[:, 0] = h2
        # Gamma^k_ij = 1/2 h^kl (d_i h_jl + d_j h_il - d_l h_ij)
        # B_ijl = d_i h_jl + d_j h_il - d_l h_ij
        B = np.zeros_like(dh)
        for i in range(3):
            for j in range(3):
                for l in range(3):
                    B[:, i, j, l] = dh[:, i, j, l] + dh[:, j, i, l] - dh[:, l, i, j]
        G = 0.5 * np.einsum("nkl,nijl->nkij", hi, B)
        # x-derivative of Gamma: d_x h^kl = -h^ka h1_ab h^bl ; d_x B uses second derivatives
        dhi = -np.einsum("nka,nab,nbl->nkl", hi, h1, hi)
        dB = np.zeros_like(B)
        for i in range(3):
            for j in range(3):
                for l in range(3):
                    dB[:, i, j, l] = ddh[:, i, j, l] + ddh[:, j, i, l] - ddh[:, l, i, j]
        dG = 0.5 * (np.einsum("nkl,nijl->nkij", dhi, B) + np.einsum("nkl,nijl->nkij", hi, dB))
        # d_m Gamma^k_ij non-zero only for m = 0
        dGm = np.zeros((n, 3, 3, 3, 3))  # [:, m, k, i, j]
        dGm[:, 0] = dG
        Ric = (np.einsum("nkkij->nij", dGm)              # d_k Gamma^k_ij
               - np.einsum("njkik->nij", dGm)            # d_j Gamma^k_ik
               + np.einsum("nkkl,nlij->nij", G, G)       # Gamma^k_kl Gamma^l_ij
               - np.einsum("nkjl,nlik->nij", G, G))      # Gamma^k_jl Gamma^l_ik
        return np.einsum("nij,nij->n", hi, Ric), G, hi

    def unpack(self, v):
        return v[0:6], v[6:9], v[9:15], v[15:18]   # h6, P_i, p6, piP^i

    def densities(self, v):
        """Return H_perp(x) and H_i(x) on the lattice."""
        h6, Pl, p6, piP = self.unpack(v)
        h = self.sym(h6)
        pi_up = self.sym(p6, scale_off=0.5)          # pi^ij from canonical p (off-diagonal p = 2 pi^ij)
        h1 = self.sym(self.D(h6))
        h2 = self.sym(self.D2(h6))
        R, G, hi = self.ricci_scalar(h, h1, h2)
        sh = np.sqrt(np.linalg.det(h))
        pi_dn = np.einsum("nia,nab,nbj->nij", h, pi_up, h)
        trpi = np.einsum("nij,nij->n", h, pi_up)
        kin = (4 * K / sh) * (np.einsum("nij,nij->n", pi_dn, pi_up) - self.cb * trpi ** 2)
        pot = (sh / (4 * K)) * (2 * self.lam - R)
        P = Pl.T                                       # (n, 3) lower index
        Pu = np.einsum("nij,nj->ni", hi, P)
        P2 = np.einsum("ni,ni->n", P, Pu)
        u = K * np.sqrt(np.maximum(P2, 0.0))
        z = u / A0
        Wser = z ** 2 / 2 + z ** 3 / 3 + z ** 4 / 4 + z ** 5 / 5
        Wfull = -z - np.log1p(-np.minimum(z, 0.999999))
        W = (A0 ** 2 / K) * np.where(z < 1e-3, Wser, Wfull)
        piPu = piP.T                                   # (n, 3) upper index density
        piP2 = np.einsum("nij,ni,nj->n", h, piPu, piPu)
        DdotP_sh = self.D(sh * Pu[:, 0])               # sqrt h D.P = d_x (sqrt h P^x)
        DdotP = DdotP_sh / sh
        F = np.zeros((self.n, 3, 3))
        for j in (1, 2):
            F[:, 0, j] = self.D(P[:, j])
            F[:, j, 0] = -F[:, 0, j]
        Fu = np.einsum("nia,njb,nab->nij", hi, hi, F)
        F2 = np.einsum("nij,nij->n", F, Fu)
        Hp = (pot + kin + piP2 / (2 * sh * ETA)
              + sh * ((GAMMA / 2) * DdotP ** 2 + W) + (GAMMA / 4) * sh * F2 + self.eps)
        if self.clock:
            Hp = Hp + DdotP_sh
        # momentum constraint: -2 D_j pi^j_i + piP^k D_i P_k - D_k(piP^k P_i)
        mixed = np.einsum("njk,nki->nji", pi_up, h)    # pi^j_i (density)
        Hi = np.zeros((self.n, 3))
        for i in range(3):
            div = self.D(mixed[:, 0, i]) - np.einsum("nkj,njk->n", G[:, :, :, i], mixed)   # - Gamma^k_{j i} pi^j_k
            DPk = np.zeros((self.n, 3))
            if i == 0:
                DPk = np.stack([self.D(P[:, k]) for k in range(3)], axis=1)
            DPk = DPk - np.einsum("nlk,nl->nk", G[:, :, i, :], P)          # D_i P_k = d_i P_k - Gamma^l_ik P_l
            term2 = np.einsum("nk,nk->n", piPu, DPk)
            term3 = self.D(piPu[:, 0] * P[:, i]) - np.einsum("nlk,nk,nl->n", G[:, :, :, i], piPu, P)
            Hi[:, i] = -2 * div + term2 - term3
        return Hp, Hi

    def H_perp(self, v):
        return self.densities(v)[0]

    def jacobian(self, v, step):
        """J[x, a, y] = d H_perp(x) / d v[a, y], central differences."""
        n = self.n
        J = np.zeros((n, 18, n))
        for a in range(18):
            for y in range(n):
                vp = v.copy(); vp[a, y] += step
                vm = v.copy(); vm[a, y] -= step
                J[:, a, y] = (self.H_perp(vp) - self.H_perp(vm)) / (2 * step)
        return J

    def grad_smeared(self, J, N):
        return self.dx * np.einsum("x,xay->ay", N, J)

    def bracket(self, gN, gM):
        """{H[N], H[M]} with q = rows 0-8 (h6, P), p = rows 9-17 (p6, piP)."""
        q, p = slice(0, 9), slice(9, 18)
        return float(np.sum(gN[q] * gM[p] - gN[p] * gM[q]) / self.dx)

    def hdot(self, J, gN):
        """{H_perp(x), H[N]} for every site x."""
        q, p = slice(0, 9), slice(9, 18)
        return (np.einsum("xay,ay->x", J[:, q], gN[p]) - np.einsum("xay,ay->x", J[:, p], gN[q])) / self.dx


def flat_state(L):
    v = np.zeros((18, L.n))
    v[0:3] = 1.0
    return v


def witness_A1(n, beta, J0=1.0, lam=0.5, clock=True):
    L = Lattice(n, beta, lam, clock=clock)
    q = np.sqrt((2 + 3 * beta) / (12 * K) * (J0 ** 2 / (2 * ETA) + lam / (2 * K)))
    v = flat_state(L)
    v[9:12] = q                                     # pi^ij = q delta^ij
    v[15] = J0                                      # piP^x = J
    return L, v, q


def witness_A3(n, beta, c=1.0, lam=0.5):
    L0 = Lattice(n, beta, lam)
    s = 1.0 + 0.3 * np.sin(L0.x) + 0.1 * np.cos(3 * L0.x)
    v = flat_state(L0)
    v[9] = c
    v[10] = s
    v[11] = s
    Hp0 = L0.H_perp(v)                               # eps = 0 here
    eps = -Hp0
    L = Lattice(n, beta, lam, eps=eps)
    pi_tr = c + 2 * s
    return L, v, eps, pi_tr, s


# ----------------------------------------------------------------------------- checks
checks, results = [], {"mutate": MUTATE, "params": {"K": K, "eta": ETA, "gamma": GAMMA, "a0": A0}}


def record(name, ok, detail):
    checks.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"{name:4s} {'PASS' if ok else 'FAIL'}  {detail}")


# R3 unit test (conformally flat, exact derivatives): R = -e^{-2s}(4 s'' + 2 s'^2)
Lt = Lattice(64, 0.0, 0.0)
sg = 0.1 * np.sin(Lt.x) + 0.05 * np.cos(2 * Lt.x)
sg1 = 0.1 * np.cos(Lt.x) - 0.1 * np.sin(2 * Lt.x)
sg2 = -0.1 * np.sin(Lt.x) - 0.2 * np.cos(2 * Lt.x)
e2 = np.exp(2 * sg)
hh = np.zeros((64, 3, 3)); h1t = np.zeros((64, 3, 3)); h2t = np.zeros((64, 3, 3))
for i in range(3):
    hh[:, i, i] = e2
    h1t[:, i, i] = 2 * sg1 * e2
    h2t[:, i, i] = (2 * sg2 + 4 * sg1 ** 2) * e2
Rt, _, _ = Lt.ricci_scalar(hh, h1t, h2t)
Rex = -np.exp(-2 * sg) * (4 * sg2 + 2 * sg1 ** 2)
r3err = float(np.max(np.abs(Rt - Rex)))
record("R0", r3err < 1e-12, f"R3 formula vs conformally-flat closed form, max |diff| = {r3err:.2e}")
results["R0"] = r3err

clock_on = not MUTATE
STEPS = (1e-5, 1e-6)

# ---- A1: Codex's witness ------------------------------------------------------------------------
A1 = {}
for beta in (0.02, 0.0):
    for n in (32, 64, 128):
        L, v, q = witness_A1(n, beta, clock=clock_on)
        Hp, Hi = L.densities(v)
        Lc, vc, _ = witness_A1(n, beta, clock=True)   # constraint residual always on the true theory
        Hpc, Hic = Lc.densities(vc)
        cres = float(max(np.max(np.abs(Hpc)), np.max(np.abs(Hic))))
        N, M = np.sin(L.x), np.cos(L.x)
        vals = []
        for st in STEPS:
            J = L.jacobian(v, st)
            vals.append(L.bracket(L.grad_smeared(J, N), L.grad_smeared(J, M)))
        pred = -(1.0 / ETA) * n * np.sin(2 * np.pi / n)
        rel = abs(vals[1] - pred) / abs(pred)
        A1[f"beta{beta}_n{n}"] = {"q": q, "constraint_residual": cres, "bracket_step1e-5": vals[0],
                                   "bracket_step1e-6": vals[1], "prediction": pred, "rel_err": rel}
        ok = cres <= 1e-12 and rel <= 1e-6
        record("A1", ok, f"beta {beta} n {n}: constraints {cres:.1e}; bracket {vals[1]:.9f} vs "
                         f"-(J/eta) n sin(2pi/n) {pred:.9f} (rel {rel:.1e}); step 1e-5 gives {vals[0]:.9f}")
results["A1"] = A1

# ---- A2: MUTATE inside the main run (clock deleted) ---------------------------------------------
A2 = {}
for n in (32, 64, 128):
    L, v, _ = witness_A1(n, 0.02, clock=False)
    J = L.jacobian(v, 1e-6)
    b = L.bracket(L.grad_smeared(J, np.sin(L.x)), L.grad_smeared(J, np.cos(L.x)))
    A2[f"n{n}"] = b
    record("A2", abs(b) <= 1e-8, f"clock deleted, n {n}: bracket {b:.2e} (must be <= 1e-8)")
results["A2"] = A2

# ---- A3: beta obstruction (P = piP = 0, non-uniform expansion, dust) ------------------------------
A3 = {}
for beta in (0.02, 0.0):
    for n in (64, 128):
        L, v, eps, pit, s = witness_A3(n, beta)
        if MUTATE:
            L.clock = False
        Hp, Hi = L.densities(v)
        cres = float(max(np.max(np.abs(Hp)), np.max(np.abs(Hi))))
        N, M = np.sin(L.x), np.cos(2 * L.x)
        J = L.jacobian(v, 1e-6)
        b = L.bracket(L.grad_smeared(J, N), L.grad_smeared(J, M))
        cpref = 2 * beta / (2 + 3 * beta)
        pred_cont = float(L.dx * np.sum(cpref * L.D(pit) * (N * L.D(M) - M * L.D(N))))
        pred_lat = float(L.dx * np.sum(4 * (1 - 2 * L.cb) * s * (M * L.D2(N) - N * L.D2(M))))
        A3[f"beta{beta}_n{n}"] = {"constraint_residual": cres, "eps_min": float(eps.min()), "bracket": b,
                                   "pred_central_diff": pred_cont, "pred_lattice_exact": pred_lat}
        if beta:
            rel = abs(b - pred_cont) / abs(pred_cont)
            A3[f"beta{beta}_n{n}"]["rel_err_vs_central"] = rel
            A3[f"beta{beta}_n{n}"]["rel_err_vs_lattice_exact"] = abs(b - pred_lat) / abs(pred_lat)
            record("A3", cres <= 1e-12 and eps.min() >= 0, f"beta {beta} n {n}: constraints {cres:.1e}, "
                   f"eps_min {eps.min():.3f}; bracket {b:.8f} vs (2b/(2+3b)) sum Dpi (N DM - M DN) "
                   f"{pred_cont:.8f} (rel {rel:.2e}); lattice-exact form {pred_lat:.8f}")
        else:
            record("A3", cres <= 1e-12 and abs(b) <= 1e-8, f"beta 0 control n {n}: bracket {b:.2e}")
r64 = A3["beta0.02_n64"]["rel_err_vs_central"]
r128 = A3["beta0.02_n128"]["rel_err_vs_central"]
record("A3", r128 <= 1e-2 and r128 < r64, f"convergence: rel err n64 {r64:.2e} -> n128 {r128:.2e}")
results["A3"] = A3

# ---- A4: tertiary form, non-constant lapse ---------------------------------------------------------
A4 = {}
for n in (64, 128):
    L, v, eps, pit, s = witness_A3(n, 0.02)
    if MUTATE:
        L.clock = False
    Nl = 1 + 0.3 * np.cos(L.x)
    J = L.jacobian(v, 1e-6)
    hd = L.hdot(J, L.grad_smeared(J, Nl))
    V = (2 * 0.02 / (2 + 3 * 0.02)) * L.D(pit)
    pred = V * L.D(Nl) + L.D(Nl * V)
    pred2 = L.D(Nl ** 2 * V) / Nl
    rel = float(np.max(np.abs(hd - pred)) / np.max(np.abs(pred)))
    rel2 = float(np.max(np.abs(hd - pred2)) / np.max(np.abs(pred2)))
    A4[f"n{n}"] = {"max_hdot": float(np.max(np.abs(hd))), "rel_err_VDN+D(NV)": rel, "rel_err_(1/N)D(N^2V)": rel2}
    record("A4", True, f"n {n}: Hdot_perp vs V DN + D(NV): rel {rel:.2e}; vs (1/N) D(N^2 V): rel {rel2:.2e}")
ra, rb = A4["n64"]["rel_err_VDN+D(NV)"], A4["n128"]["rel_err_VDN+D(NV)"]
record("A4", rb <= 1e-2 and rb < ra, f"convergence: {ra:.2e} -> {rb:.2e}")
results["A4"] = A4

# ---- A5: integral identity (sympy) + its lattice version -------------------------------------------
x, y, z = sp.symbols("x y z", real=True)
Ns = 1 + sp.Rational(1, 3) * sp.cos(x) + sp.Rational(1, 5) * sp.sin(2 * x)
pis = sp.Rational(2, 7) * sp.sin(x) + sp.Rational(1, 4) * sp.cos(3 * x)
lhs = sp.integrate(pis * sp.diff(Ns ** 2 * sp.diff(pis, x), x), (x, 0, 2 * sp.pi))
rhs = -sp.integrate(Ns ** 2 * sp.diff(pis, x) ** 2, (x, 0, 2 * sp.pi))
id1 = sp.simplify(lhs - rhs)
N3 = 1 + sp.Rational(1, 4) * sp.cos(x) * sp.sin(y) + sp.Rational(1, 6) * sp.cos(z)
p3 = sp.sin(x) + sp.Rational(1, 2) * sp.cos(y) * sp.sin(z)
lhs3 = sum(sp.integrate(sp.integrate(sp.integrate(
    sp.expand(p3 * sp.diff(N3 ** 2 * sp.diff(p3, w), w)), (x, 0, 2 * sp.pi)), (y, 0, 2 * sp.pi)), (z, 0, 2 * sp.pi))
    for w in (x, y, z))
rhs3 = -sum(sp.integrate(sp.integrate(sp.integrate(
    sp.expand(N3 ** 2 * sp.diff(p3, w) ** 2), (x, 0, 2 * sp.pi)), (y, 0, 2 * sp.pi)), (z, 0, 2 * sp.pi))
    for w in (x, y, z))
id3 = sp.simplify(lhs3 - rhs3)
L, v, eps, pit, s = witness_A3(128, 0.02)
Vv = L.D(pit)
Nl = 1 + 0.3 * np.cos(L.x)
lat = float(np.sum(pit * L.D(Nl ** 2 * Vv)) + np.sum(L.D(pit) * Nl ** 2 * Vv))
record("A5", id1 == 0 and id3 == 0 and abs(lat) < 1e-10,
       f"int pi d(N^2 d pi) + int N^2 |d pi|^2 = {id1} (1D), {id3} (3D); lattice summation by parts {lat:.1e}; "
       f"value of int N^2 |d pi|^2 (1D) = {float(-rhs):.4f} > 0")
results["A5"] = {"identity_1D": str(id1), "identity_3D": str(id3), "lattice_sbp": lat, "int_N2_dpi2_1D": float(-rhs)}

# ---- A6: linear Dirac algorithm on Minkowski, scalar sector --------------------------------------
X = sp.symbols("X", real=True)
Ks, eta, gam, beta, k = sp.symbols("K eta gamma beta k", positive=True)
cb = (1 + beta) / (2 + 3 * beta)
cpre = 2 * beta / (2 + 3 * beta)
a, b, P, n_, s_ = [sp.Function(nm)(X) for nm in ("a", "b", "P", "n", "s")]
pa, pb, Pi, pn, ps = [sp.Function(nm)(X) for nm in ("p_a", "p_b", "Pi", "p_n", "p_s")]
Q = [a, b, P, n_, s_]
Pm = [pa, pb, Pi, pn, ps]
eps_ = sp.symbols("epsilon")
# (sqrt h R3) to second order for h = diag(1 + a, 1 + b, 1 + b)(X)
hm = sp.diag(1 + eps_ * a, 1 + eps_ * b, 1 + eps_ * b)
hinv = hm.inv()
coords = [X, sp.Symbol("Y"), sp.Symbol("Z")]
Gam = [[[sum(hinv[kk, l] * (sp.diff(hm[j, l], coords[i]) + sp.diff(hm[i, l], coords[j]) - sp.diff(hm[i, j], coords[l]))
             for l in range(3)) / 2 for j in range(3)] for i in range(3)] for kk in range(3)]
Ric = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        Ric[i, j] = (sum(sp.diff(Gam[kk][i][j], coords[kk]) for kk in range(3))
                     - sum(sp.diff(Gam[kk][i][kk], coords[j]) for kk in range(3))
                     + sum(Gam[kk][kk][l] * Gam[l][i][j] for kk in range(3) for l in range(3))
                     - sum(Gam[kk][j][l] * Gam[l][i][kk] for kk in range(3) for l in range(3)))
Rs = sum(hinv[i, j] * Ric[i, j] for i in range(3) for j in range(3))
shR = sp.series(sp.sqrt(hm.det()) * Rs, eps_, 0, 3).removeO()
R1 = sp.simplify(shR.coeff(eps_, 1))
R2 = sp.simplify(shR.coeff(eps_, 2))
clock_lin = 0 if MUTATE else 1
H1 = -R1 / (4 * Ks) + clock_lin * sp.diff(P, X)                       # first-order H_perp
Hx1 = -2 * sp.diff(pa, X)                                              # first-order H_x
Hdens = (-R2 / (4 * Ks) + 4 * Ks * (pa ** 2 + pb ** 2 / 2 - cb * (pa + pb) ** 2) + Pi ** 2 / (2 * eta)
         + gam / 2 * sp.diff(P, X) ** 2 + Ks * P ** 2 / 2 + n_ * H1 + s_ * Hx1)


def vder(dens, f, order=4):
    out = sp.diff(dens, f)
    for m in range(1, order + 1):
        out += (-1) ** m * sp.diff(sp.diff(dens, sp.Derivative(f, (X, m))), X, m)
    return sp.expand(out)


dHdq = {f: vder(Hdens, f) for f in Q}
dHdp = {f: vder(Hdens, f) for f in Pm}


def coeffs(C, f, order=6):
    """{m: coefficient of d^m f} for a density C linear in the fields."""
    out = {}
    for m in range(order, 0, -1):
        cm = sp.diff(C, sp.Derivative(f, (X, m)))
        if cm != 0:
            out[m] = cm
            C = sp.expand(C - cm * sp.Derivative(f, (X, m)))
    c0 = sp.diff(C, f)
    if c0 != 0:
        out[0] = c0
    return out


def tdot(C):
    """{C(x), H} for a density linear in fields."""
    res = 0
    for qf, pf in zip(Q, Pm):
        for m, cm in coeffs(C, qf).items():
            res += cm * sp.diff(dHdp[pf], X, m)
        for m, cm in coeffs(C, pf).items():
            res -= cm * sp.diff(dHdq[qf], X, m)
    return sp.expand(res)


def symbol(C1, C2):
    """Fourier symbol of {C1(x), C2(y)} with d_x -> i k, d_y -> -i k."""
    tot = 0
    for qf, pf in zip(Q, Pm):
        c1q, c1p = coeffs(C1, qf), coeffs(C1, pf)
        c2q, c2p = coeffs(C2, qf), coeffs(C2, pf)
        s1q = sum(c * (sp.I * k) ** m for m, c in c1q.items())
        s1p = sum(c * (sp.I * k) ** m for m, c in c1p.items())
        s2q = sum(c * (-sp.I * k) ** m for m, c in c2q.items())
        s2p = sum(c * (-sp.I * k) ** m for m, c in c2p.items())
        tot += s1q * s2p - s1p * s2q
    return sp.simplify(tot)


chi0 = tdot(H1)
chi_target = cpre * sp.diff(pa + pb, X, 2) + clock_lin * sp.diff(Pi, X) / eta
rem0 = sp.expand(chi0 - chi_target)
lam_val = sp.simplify(sp.diff(rem0, sp.Derivative(pa, (X, 2))) / (-2))      # d_x H_x = -2 p_a''
rem_ok = sp.simplify(rem0 - lam_val * sp.diff(Hx1, X)) == 0
chi = chi_target
psi = tdot(chi)
Zk = Ks * (2 + 3 * beta) / beta + eta * k ** 2
sym_chi_H1 = symbol(chi, H1)
sym_pn_psi = symbol(pn, psi)
ratio1 = sp.simplify(sym_chi_H1 / (k ** 2 * Zk)) if sym_chi_H1 != 0 else 0
ratio2 = sp.simplify(sym_pn_psi / (k ** 2 * Zk)) if sym_pn_psi != 0 else 0
cons = [pn, ps, H1, Hx1, chi, psi]
names = ["pi_n", "pi_s", "H_perp", "H_x", "chi", "psi"]
Mx = sp.zeros(6, 6)
for i in range(6):
    for j in range(6):
        Mx[i, j] = symbol(cons[i], cons[j])
rank_generic = Mx.subs({Ks: 1, eta: sp.Rational(7, 5), gam: sp.Rational(3, 10), beta: sp.Rational(1, 50),
                        k: sp.Rational(13, 10)}).rank()
fc_rows = [names[i] for i in range(6) if all(sp.simplify(Mx[i, j]) == 0 for j in range(6))]
pf = sp.simplify(Mx[0, 5] * Mx[2, 4] - Mx[0, 4] * Mx[2, 5] + Mx[0, 2] * Mx[4, 5])  # Pfaffian of {pi_n, H, chi, psi}
dof = sp.Rational(10 - 2 * len(fc_rows) - rank_generic, 2)
ok6 = (rem_ok and ratio1 != 0 and not ratio1.has(k) and ratio2 != 0 and not ratio2.has(k)
       and rank_generic == 4 and sorted(fc_rows) == ["H_x", "pi_s"] and dof == 1)
record("A6", ok6, f"chi0 = chi_target + ({lam_val}) d_x H_x: {rem_ok}; {{chi,H_perp}} = ({ratio1}) k^2 Z; "
                  f"{{pi_n,psi}} = ({ratio2}) k^2 Z; bracket-matrix rank {rank_generic}; first-class rows {fc_rows}; "
                  f"scalar-sector DOF {dof}")
results["A6"] = {"R1": str(R1), "R2": str(R2), "chi0": str(chi0), "chi": str(chi), "lambda": str(lam_val),
                 "psi_lapse_part": str(sp.collect(sp.expand(psi), [sp.Derivative(n_, (X, 4)), sp.Derivative(n_, (X, 2))])),
                 "sym_chi_H1": str(sym_chi_H1), "sym_pn_psi": str(sym_pn_psi), "ratio_chi_H1_over_k2Z": str(ratio1),
                 "ratio_pn_psi_over_k2Z": str(ratio2), "matrix": [[str(sp.simplify(Mx[i, j])) for j in range(6)] for i in range(6)],
                 "names": names, "rank_generic": int(rank_generic), "first_class_rows": fc_rows,
                 "pfaffian_block": str(pf), "scalar_dof": str(dof)}

npass = sum(c["pass"] for c in checks)
results["checks"] = checks
results["summary"] = f"{npass}/{len(checks)} PASS"
print(results["summary"])
with open(OUT, "w") as fh:
    json.dump(results, fh, indent=1, default=str)
sys.exit(0 if npass == len(checks) else 1)
