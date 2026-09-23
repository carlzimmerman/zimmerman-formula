#!/usr/bin/env python3
"""L326 gauge-model instance: exact diagonalisation of ONE SU(2) Kogut-Susskind plaquette in the FULL (not
gauge-projected) truncated Hilbert space, H = (x/2) sum_l C_l + (b/x)(1 - Re Tr U_p / 2).

Link space: Peter-Weyl basis |j m n>, j <= jmax; C|j m n> = j(j+1)|j m n>; multiplication by the fundamental matrix
element U_ab: U_ab|j m n> = sum_{J = j +/- 1/2} sqrt((2j+1)/(2J+1)) <1/2 a; j m|J a+m> <1/2 b; j n|J b+n> |J a+m, b+n>
(compressed to j <= jmax).  (U^dagger)_cd = multiplication by conj(U_dc) = adjoint of multiplication by U_dc.
U_p = U1 U2 U3^dag U4^dag.

The theorem (DERIVATION.md, D = 1 for a single plaquette, link sites s = 4) says: for x >= X = sqrt((2b/C_F) D / lam_c)
the gap is >= x C_F / 4, i.e. the NORMALISED gap (E1 - E0)/(x C_F/2) >= 1/2.  A normalised gap < 1/2 anywhere above X
would FALSIFY it.  HONEST SCOPE: a single plaquette has no breakdown -- its normalised gap stays near 1 wherever the truncation has
converged (jmax 1/2 vs 1 agree to < 1%), so this instance is CONSISTENT but NON-DISCRIMINATING; small-x values are
truncation artifacts and are not used.  The discriminating tests of the lemmas are the referee toys (referee*.py).
"""
import sys, math, json, os
import numpy as np
import scipy.sparse as sp
from scipy.sparse.linalg import eigsh
from sympy.physics.quantum.cg import CG
from sympy import S

LAM_C4 = 2977072941 / 250000000000
CF = 0.75


def basis(jmax2):                        # j in half-integers: store 2j
    B = []
    for j2 in range(0, jmax2 + 1):
        for m2 in range(-j2, j2 + 1, 2):
            for n2 in range(-j2, j2 + 1, 2):
                B.append((j2, m2, n2))
    return B, {b: i for i, b in enumerate(B)}


def cg(j1_2, m1_2, j2_2, m2_2, J2, M2):
    return float(CG(S(j1_2) / 2, S(m1_2) / 2, S(j2_2) / 2, S(m2_2) / 2, S(J2) / 2, S(M2) / 2).doit())


def mult_U(jmax2):
    """dict (a2, b2) -> sparse matrix of multiplication by U_ab (a2, b2 in {+1, -1})."""
    B, idx = basis(jmax2)
    out = {}
    for a2 in (1, -1):
        for b2 in (1, -1):
            rows, cols, vals = [], [], []
            for i, (j2, m2, n2) in enumerate(B):
                for J2 in (j2 + 1, j2 - 1):
                    if J2 < 0 or J2 > jmax2:
                        continue
                    M2, N2 = m2 + a2, n2 + b2
                    if abs(M2) > J2 or abs(N2) > J2:
                        continue
                    c = math.sqrt((j2 + 1) / (J2 + 1)) * cg(1, a2, j2, m2, J2, M2) * cg(1, b2, j2, n2, J2, N2)
                    if abs(c) > 1e-14:
                        rows.append(idx[(J2, M2, N2)]); cols.append(i); vals.append(c)
            out[(a2, b2)] = sp.csr_matrix((vals, (rows, cols)), shape=(len(B), len(B)))
    cas = sp.diags([(j2 / 2) * (j2 / 2 + 1) for (j2, _, _) in B])
    return out, cas, len(B)


def kron4(A, B_, C, D):
    return sp.kron(sp.kron(sp.kron(A, B_, format="csr"), C, format="csr"), D, format="csr")


def build(jmax2):
    U, cas, d = mult_U(jmax2)
    I = sp.identity(d, format="csr")
    Udag = {(c, dd): U[(dd, c)].conj().T.tocsr() for c in (1, -1) for dd in (1, -1)}
    TrUp = None
    for a in (1, -1):
        for b in (1, -1):
            for c in (1, -1):
                for e in (1, -1):
                    term = kron4(U[(a, b)], U[(b, c)], Udag[(c, e)], Udag[(e, a)])
                    TrUp = term if TrUp is None else TrUp + term
    ReTr = 0.5 * (TrUp + TrUp.conj().T)
    Cs = kron4(cas, I, I, I) + kron4(I, cas, I, I) + kron4(I, I, cas, I) + kron4(I, I, I, cas)
    one = sp.identity(d ** 4, format="csr")
    return Cs.tocsr(), (one - 0.5 * ReTr).tocsr(), d


def gap(Cs, Mp, x, b):
    H = (x / 2) * Cs + (b / x) * Mp
    w = eigsh(H, k=3, which="SA", return_eigenvectors=False, tol=1e-10)
    w = np.sort(w)
    return (w[1] - w[0]) / (x * CF / 2), w


if __name__ == "__main__":
    res = {}
    ok = True
    for b in (2.0, 4.0):
        X = math.sqrt((2 * b / CF) * 1 / LAM_C4)
        res[f"b={b}"] = {"X_theorem_D1": X}
        print(f"\n== b = {b}: theorem threshold (D = 1, link sites) X = {X:.2f} ==")
        for jmax2 in (1, 2):
            Cs, Mp, d = build(jmax2)
            xs = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0, 10.0, X, 1.5 * X, 3 * X]
            gs = []
            for x in xs:
                g, w = gap(Cs, Mp, x, b)
                gs.append(g)
                print(f"   jmax = {jmax2/2:3.1f} (dim {d**4:6d})  x = {x:7.2f}  normalised gap = {g:.4f}")
            above = [g for x, g in zip(xs, gs) if x >= X]
            if min(above) < 0.5:
                ok = False
            res[f"b={b}"][f"jmax={jmax2/2}"] = {"x": xs, "gap_norm": gs}
            if jmax2 == 2:
                prev = res[f"b={b}"]["jmax=0.5"]["gap_norm"]
                conv = [(x, g, abs(g - g0) / g) for x, g, g0 in zip(xs, gs, prev)]
                conv_ok = [(x, g) for x, g, dd in conv if dd < 0.01]          # jmax 1/2 -> 1 changes < 1%
                xmin_conv = min(x for x, _ in conv_ok)
                gmin_conv = min(g for _, g in conv_ok)
                res[f"b={b}"]["truncation_converged_from_x"] = xmin_conv
                res[f"b={b}"]["min_gap_norm_converged"] = gmin_conv
                print(f"   truncation-converged (<1% between jmax 1/2 and 1) for x >= {xmin_conv:.2f}; there the "
                      f"normalised gap >= {gmin_conv:.4f} -- far above 1/2: consistent, NON-discriminating "
                      f"(a single plaquette never approaches the bound in the converged range)")
    # truncation convergence spot-check at jmax = 3/2 (810k states, ~2e8 nonzeros: opt-in with J32=1)
    Cs, Mp, d = build(3) if os.environ.get("J32") == "1" else (None, None, 0)
    for x in ((1.0, 3.0, 21.16) if Cs is not None else ()):
        g3 = gap(Cs, Mp, x, 2.0)[0]
        res.setdefault("jmax=1.5_b=2", {})[f"x={x}"] = g3
        print(f"   jmax = 1.5 (dim {d**4}) x = {x:6.2f}  normalised gap = {g3:.4f}")
    res["theorem_holds_on_instance"] = ok
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "gauge_instance_results.json"), "w"), indent=1)
    print("\nTHEOREM HOLDS ON THIS INSTANCE (normalised gap >= 1/2 for every x >= X):", ok)
    sys.exit(0 if ok else 1)
