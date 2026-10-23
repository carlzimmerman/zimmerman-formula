#!/usr/bin/env python3
"""Codex arrival audit A7 (AMENDMENT A2): constraint-bracket rank of DSF-21 / A33 on a moving-P background.

Reduced scalar sector, k || x: h = diag(1+a, 1+b, 1+b)(x), P = (P(x), 0, 0), lapse N(x), shift (s(x), 0, 0), momenta
p_a = pi^xx, p_b = 2 pi^yy (= 2 pi^zz), Pi = pi_P^x, p_N, p_s.  Everything is exact in the fields (no linearisation)
until the final step; W is kept as K P^2/(2(1+a)) (u^2 term), which fixes all second derivatives at P = 0.

chi := {H_perp(x), H_T} with H_T = int (N H_perp + s H_x).  Background = Codex's witness (A1): a = b = P = 0,
p_a = q, p_b = 2q, Pi = J, N = 1, s = 0, q from H_perp = 0.  The constraints {p_N, p_s, H_perp, H_x, chi} are
linearised there and their Fourier bracket matrix M(k) is formed (d_x -> ik on the first slot, -ik on the second).
--mutate deletes the clock term.
"""
import json
import sys

import sympy as sp

MUTATE = "--mutate" in sys.argv
BPS = "--bps" in sys.argv          # A8: add alpha a_i a^i (Blanchet-Pujolas-Sibiryakov) to the Lagrangian
X = sp.symbols("X", real=True)
K, eta, gam, beta, lam, J, k, alpha = sp.symbols("K eta gamma beta Lambda J k alpha", positive=True)
cb = (1 + beta) / (2 + 3 * beta)
names_q = ["a", "b", "P", "N", "s"]
names_p = ["p_a", "p_b", "Pi", "p_N", "p_s"]
Q = [sp.Function(n)(X) for n in names_q]
Pm = [sp.Function(n)(X) for n in names_p]
a, b, P, N, s = Q
pa, pb, Pi, pN, ps = Pm

# ---- exact reduced densities -----------------------------------------------------------------
hm = sp.diag(1 + a, 1 + b, 1 + b)
hinv = hm.inv()
crd = [X, sp.Symbol("Y"), sp.Symbol("Z")]
Gam = [[[sp.simplify(sum(hinv[kk, l] * (sp.diff(hm[j, l], crd[i]) + sp.diff(hm[i, l], crd[j]) - sp.diff(hm[i, j], crd[l]))
                         for l in range(3)) / 2) for j in range(3)] for i in range(3)] for kk in range(3)]
Ric = sp.zeros(3, 3)
for i in range(3):
    for j in range(3):
        Ric[i, j] = (sum(sp.diff(Gam[kk][i][j], crd[kk]) for kk in range(3))
                     - sum(sp.diff(Gam[kk][i][kk], crd[j]) for kk in range(3))
                     + sum(Gam[kk][kk][l] * Gam[l][i][j] for kk in range(3) for l in range(3))
                     - sum(Gam[kk][j][l] * Gam[l][i][kk] for kk in range(3) for l in range(3)))
R3 = sp.simplify(sum(hinv[i, j] * Ric[i, j] for i in range(3) for j in range(3)))
sh = sp.sqrt(1 + a) * (1 + b)
pi_sq = (1 + a) ** 2 * pa ** 2 + 2 * (1 + b) ** 2 * (pb / 2) ** 2
pi_tr = (1 + a) * pa + (1 + b) * pb
shDP = sp.diff((1 + b) * P / sp.sqrt(1 + a), X)          # sqrt h D.P
DP = shDP / sh
clock = 0 if MUTATE else 1
Hperp = ((sh / (4 * K)) * (2 * lam - R3) + (4 * K / sh) * (pi_sq - cb * pi_tr ** 2) + (1 + a) * Pi ** 2 / (2 * sh * eta)
         + clock * shDP + (gam / 2) * sh * DP ** 2 + sh * K * P ** 2 / (2 * (1 + a)))
Hx = -2 * sp.diff((1 + a) * pa, X) + sp.diff(a, X) * pa + sp.diff(b, X) * pb - sp.diff(Pi, X) * P
HT = N * Hperp + s * Hx
if BPS:
    HT = HT - alpha * sh * sp.diff(N, X) ** 2 / (N * (1 + a))   # -N sqrt(h) alpha h^xx (d ln N)^2


def derivs_in(expr, f, maxm=8):
    return [m for m in range(maxm, -1, -1) if expr.has(sp.Derivative(f, (X, m)) if m else f)]


def vder(dens, f, maxm=6):
    out = sp.diff(dens, f)
    for m in range(1, maxm + 1):
        dm = sp.Derivative(f, (X, m))
        if dens.has(dm):
            out += (-1) ** m * sp.diff(sp.diff(dens, dm), X, m)
    return out


dHq = {f: vder(HT, f) for f in Q}
dHp = {f: vder(HT, f) for f in Pm}


def pb_with_HT(C, maxm=8):
    """{C(x), H_T} for a nonlinear local density C."""
    res = 0
    for qf, pf in zip(Q, Pm):
        for m in range(maxm + 1):
            dq = sp.Derivative(qf, (X, m)) if m else qf
            dp = sp.Derivative(pf, (X, m)) if m else pf
            if C.has(dq):
                res += sp.diff(C, dq) * sp.diff(dHp[pf], X, m)
            if C.has(dp):
                res -= sp.diff(C, dp) * sp.diff(dHq[qf], X, m)
    return res


chi = pb_with_HT(Hperp)
CN = vder(HT, N)                      # secondary from p_N (= H_perp without the BPS term)

# ---- background and linearisation ---------------------------------------------------------------
q = sp.sqrt((2 + 3 * beta) / (12 * K) * (J ** 2 / (2 * eta) + lam / (2 * K)))
bg = {a: 0, b: 0, P: 0, N: 1, s: 0, pa: q, pb: 2 * q, Pi: J, pN: 0, ps: 0}
dQ = [sp.Function("d" + n)(X) for n in names_q]
dP = [sp.Function("d" + n)(X) for n in names_p]
ep = sp.symbols("ep")


def linearise(C):
    sub = {f: bg[f] + ep * df for f, df in zip(Q + Pm, dQ + dP)}
    Cs = C.subs(sub).doit()
    return sp.expand(sp.simplify(sp.diff(Cs, ep).subs(ep, 0)))


def coeffs(C, f, maxm=8):
    out = {}
    for m in range(maxm, 0, -1):
        dm = sp.Derivative(f, (X, m))
        if C.has(dm):
            out[m] = sp.diff(C, dm)
            C = sp.expand(C - out[m] * dm)
    if C.has(f):
        out[0] = sp.diff(C, f)
    return out


def symbol(C1, C2):
    tot = 0
    for qf, pf in zip(dQ, dP):
        c1q, c1p, c2q, c2p = coeffs(C1, qf), coeffs(C1, pf), coeffs(C2, qf), coeffs(C2, pf)
        s1q = sum(c * (sp.I * k) ** m for m, c in c1q.items())
        s1p = sum(c * (sp.I * k) ** m for m, c in c1p.items())
        s2q = sum(c * (-sp.I * k) ** m for m, c in c2q.items())
        s2p = sum(c * (-sp.I * k) ** m for m, c in c2p.items())
        tot += s1q * s2p - s1p * s2q
    return sp.simplify(tot)


bg_res = {"H_perp": sp.simplify(Hperp.subs(bg).doit()), "H_x": sp.simplify(Hx.subs(bg).doit()),
          "chi" if not BPS else "C_N": sp.simplify((chi if not BPS else CN).subs(bg).doit())}
cons_full = [pN, ps, Hperp, Hx, chi] if not BPS else [pN, ps, CN, Hx]
names = ["p_N", "p_s", "H_perp", "H_x", "chi"] if not BPS else ["p_N", "p_s", "C_N", "H_x"]
NC = len(cons_full)
lin = [linearise(C) for C in cons_full]
M = sp.zeros(NC, NC)
for i in range(NC):
    for j in range(NC):
        M[i, j] = symbol(lin[i], lin[j])

checks, out = [], {"mutate": MUTATE}


def record(name, ok, detail):
    checks.append({"check": name, "pass": bool(ok), "detail": detail})
    print(f"{name:4s} {'PASS' if ok else 'FAIL'}  {detail}")


num = {K: 1, eta: 1, gam: sp.Rational(3, 10), beta: sp.Rational(1, 50), lam: sp.Rational(1, 2), alpha: sp.Rational(1, 3)}
bgok = all(sp.simplify(v.subs(num).subs(J, 1)) == 0 for v in bg_res.values())
record("A7", bgok, f"background on all constraints incl. chi at J = 1: {[str(sp.simplify(v.subs(num).subs(J, 1))) for v in bg_res.values()]}")
s_pn_chi = sp.simplify(M[0, NC - 1] if not BPS else M[0, 2])
record("A7", True, f"symbol {{p_N, {names[NC - 1] if not BPS else 'C_N'}}} = {s_pn_chi}")
zero_rows = [names[i] for i in range(NC) if all(sp.simplify(M[i, j]) == 0 for j in range(NC))]
record("A7", True, f"identically vanishing rows (first class at this point): {zero_rows}")
ranks = {}
for Jv in (1, sp.Rational(1, 10), sp.Rational(1, 1000), 0):
    for kv in (sp.Rational(7, 10), sp.Rational(13, 10), 3):
        Mn = M.subs(num).subs({J: Jv, k: kv})
        ranks[f"J={Jv},k={kv}"] = int(Mn.rank(simplify=True))
record("A7", True, "complex rank of M(k): " + ", ".join(f"{kk}: {v}" for kk, v in ranks.items()))
blk = M.extract([0, 2, 4], [0, 2, 4]) if not BPS else M.extract([0, 2], [0, 2])
det_blk = sp.factor(sp.simplify(blk.det()))
r_J1 = ranks["J=1,k=13/10"]
dof_J1 = sp.Rational(10 - 2 * (NC - r_J1) - r_J1, 2)
r_J0 = ranks["J=0,k=13/10"]
dof_J0 = sp.Rational(10 - 2 * (NC - r_J0) - r_J0, 2) if BPS else None
record("A7", True, f"det of {'{p_N, H_perp, chi}' if not BPS else '{p_N, C_N}'} block = {det_blk}; scalar DOF per mode "
                   f"at J = 1: {dof_J1}" + (f"; at J = 0 (chain stops at C_N): {dof_J0}" if BPS else " (A6, Minkowski: 1)"))
out.update({"bg_residuals": {k_: str(v) for k_, v in bg_res.items()}, "q": str(q),
            "linearised": {n_: str(c) for n_, c in zip(names, lin)},
            "M": [[str(sp.simplify(M[i, j])) for j in range(NC)] for i in range(NC)], "names": names, "bps": BPS,
            "sym_pN_chi": str(s_pn_chi), "zero_rows": zero_rows, "ranks": ranks, "det_block": str(det_blk),
            "dof_per_mode_J1": str(dof_J1), "checks": checks})
with open("r1_rank_moving_P" + ("_BPS" if BPS else "") + ("_MUTATE" if MUTATE else "") + ".json", "w") as fh:
    json.dump(out, fh, indent=1)
print("done")
