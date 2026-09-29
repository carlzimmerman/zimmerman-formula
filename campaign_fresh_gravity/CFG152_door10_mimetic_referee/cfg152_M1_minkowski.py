#!/usr/bin/env python3
"""CFG152 M1 (Minkowski, exact in k): method M1, controls C0, C1, C4, numerics N1 and the headline H on Minkowski.

Frozen criteria: ../CFG152_FROZEN_CRITERIA.md (sha256 printed first).  Modes: MUTATE unset (main), a, b, 1.
Run:  python3 cfg152_M1_minkowski.py            (main)
      MUTATE=a python3 cfg152_M1_minkowski.py   (and b, 1)
Writes cfg152_M1_minkowski[_MUTATE_<mode>].out and ..._results.json next to this file.
"""
import random
import sys

import mpmath as mp
import numpy as np
import sympy as sp
from sympy.calculus.euler import euler_equations

import cfg152_common as C
from cfg152_common import Mp2, gt, k, t, w, x

NAME = "cfg152_M1_minkowski"
mode = C.get_mode(["main", "a", "b", "1"])
rep = C.Report(NAME, mode)
C.header(rep)
cbox = C.c_box_for(mode)
rep.p(f"c_box = {cbox}   (main run: gt*Mp2/2, i.e. CFG124's +(gamma/2)(box phi)^2 with gt = gamma/M_P^2)")
HEAD = gt / (2 - 3 * gt)          # the headline form under test (CFG124 README)
rep.p(f"headline form under test: c_s^2 = {HEAD}; ghost window 0 < gt < 2/3")
R = rep.results


def zero_exact(expr, samplers, n=30):
    """Spec: 'exactly' = sympy simplify gives 0; else 30 random rational points at 50 digits with |diff| < 1e-40."""
    e = sp.simplify(expr)
    if e == 0:
        return True, "simplify"
    rng = random.Random(152)
    for _ in range(n):
        vals = {s: f(rng) for s, f in samplers.items()}
        v = sp.N(e.subs(vals), 50)
        if abs(v) > sp.Float("1e-40"):
            return False, f"nonzero: {e} (e.g. {v} at {vals})"
    return True, "30 random rational points at 50 digits (simplify did not return 0)"


SAMP = {gt: lambda r: sp.Rational(r.randint(-10**6, 10**6), r.randint(1, 10**6)) + sp.Rational(1, 7919),
        k: lambda r: sp.Rational(r.randint(1, 10**6), r.randint(1, 10**6)),
        Mp2: lambda r: sp.Rational(r.randint(1, 10**6), r.randint(1, 10**6))}

# ------------------------------------------------------------------ 1. expansion
rep.p("\n== 1. brute-force second-order expansion about Minkowski (phi = t, lambda = 0, V = 0)")
o = C.expand_action("mink", cbox, log=rep.p)
F = o["fields"]
order = C.FIELD_NAMES                       # Phi, B, Psi, E, dphi, dlam, h
fl = [F[n] for n in order]
rep.check("internal: expansion checks (det, R_bar = 0, box phi two ways agree)", all(o["checks"].values()),
          o["checks"], kind="internal")
rep.check("internal: zeroth-order Lagrangian vanishes", sp.simplify(o["L0"]) == 0, kind="internal")
els = euler_equations(o["L1"], fl, [t, x])
tad = [sp.simplify(e.lhs) for e in els]
rep.check("internal: Minkowski with phi = t, lambda = 0, V = 0 is a solution (all first-order EL terms vanish)",
          all(v == 0 for v in tad), tad, kind="internal")

# ------------------------------------------------------------------ 2. Fourier matrix
rep.p("\n== 2. Fourier Hermitian form M(omega, k) in (Phi, B, Psi, E, dphi, dlam, h)")
M = C.fourier_matrix(o["L2"], fl)
rep.check("internal: M is Hermitian", sp.simplify(M - M.H) == sp.zeros(7, 7), kind="internal")
iH = order.index("h")
dec = all(sp.simplify(M[iH, j]) == 0 and sp.simplify(M[j, iH]) == 0 for j in range(7) if j != iH)
rep.check("internal: the tensor mode h decouples from the scalars", dec, kind="internal")
for i in range(7):
    for j in range(i, 7):
        if M[i, j] != 0:
            rep.p(f"   M[{order[i]},{order[j]}] = {sp.factor(M[i, j])}")
R["M_entries"] = {f"{order[i]},{order[j]}": str(sp.factor(M[i, j])) for i in range(7) for j in range(i, 7) if M[i, j] != 0}

# ------------------------------------------------------------------ 3. step (i): gauge vectors
rep.p("\n== 3. step (i): scalar gauge vectors from -Lie_xi of the background")
gv = C.lie_gauge_vectors(order)
for v, nm in zip(gv, ("xi0", "zeta")):
    rep.p(f"   gauge vector ({nm}): {list(v)}")
res = [sp.simplify(M * v) for v in gv]
rep.check("step (i): both scalar gauge vectors are null vectors of M for all omega, k, gt",
          all(r_ == sp.zeros(7, 1) for r_ in res), [list(r_) for r_ in res], kind="method check")


def sub(Mx, names, ordr):
    ids = [ordr.index(n) for n in names]
    return Mx.extract(ids, ids)


# ------------------------------------------------------------------ 4. step (ii): two complete gauges
rep.p("\n== 4. step (ii): det of M in unitary (dphi = E = 0) and Newtonian (B = E = 0) gauge")
MU = sub(M, ["Phi", "B", "Psi", "dlam"], order)
MN = sub(M, ["Phi", "Psi", "dphi", "dlam"], order)
detU = sp.factor(sp.expand(MU.det(method="berkowitz")))
detN = sp.factor(sp.expand(MN.det(method="berkowitz")))
rep.p(f"   det_unitary   = {detU}")
rep.p(f"   det_Newtonian = {detN}")
R["det_unitary"], R["det_newtonian"] = str(detU), str(detN)
mU, PU = C.poly_in_w(detU)
mN, PN = C.poly_in_w(detN)
rep.p(f"   zero roots: unitary omega^{mU}, Newtonian omega^{mN}; remaining polynomials: {PU.as_expr()} | {PN.as_expr()}")
R["zero_root_multiplicity"] = {"unitary": mU, "newtonian": mN}


def cs2_from_poly(P):
    cf = P.all_coeffs()[::-1]
    if P.degree() != 2 or sp.simplify(cf[1]) != 0:
        return None
    return sp.simplify(-cf[0] / (cf[2] * k**2))


cs2U, cs2N = cs2_from_poly(PU), cs2_from_poly(PN)
same = sp.simplify(PU.as_expr() / PN.as_expr())
rep.check("step (ii): the nonzero roots agree between the two gauges (ratio of the reduced dets is omega-free)",
          not same.has(w), f"ratio = {same}", kind="method check")
rep.p(f"   c_s^2 (unitary det) = {cs2U};  c_s^2 (Newtonian det) = {cs2N}")
R["cs2_det_unitary"], R["cs2_det_newtonian"] = str(cs2U), str(cs2N)
okU = cs2U is not None and zero_exact(cs2U - HEAD, {gt: SAMP[gt]})[0]
okN = cs2N is not None and zero_exact(cs2N - HEAD, {gt: SAMP[gt]})[0]
rep.check("H-a (M1 step ii, unitary gauge): c_s^2 = gt/(2 - 3 gt) exactly", okU, cs2U)
rep.check("H-a (M1 step ii, Newtonian gauge): c_s^2 = gt/(2 - 3 gt) exactly", okN, cs2N)

# ------------------------------------------------------------------ 5. step (iii): Schur complement
rep.p("\n== 5. step (iii): unitary gauge, eliminate dlam, Phi, B by their own equations (Schur complement)")
ordU = ["Phi", "B", "Psi", "dlam"]
P_, A_ = [ordU.index("Psi")], [ordU.index(n) for n in ("Phi", "B", "dlam")]
MAA = MU.extract(A_, A_)
detAA = sp.factor(MAA.det())
rep.p(f"   det of the auxiliary block (Phi, B, dlam) = {detAA}")
Mred = sp.cancel(sp.simplify((MU.extract(P_, P_) - MU.extract(P_, A_) * MAA.inv() * MU.extract(A_, P_))[0, 0]))
num, den = sp.fraction(sp.together(Mred))
rep.p(f"   M_red(omega, k) = {sp.factor(Mred)}")
R["M_red"] = str(sp.factor(Mred))
PR = sp.Poly(sp.expand(num), w)
cf = PR.all_coeffs()[::-1]
form_ok = (not den.has(w)) and PR.degree() == 2 and sp.simplify(cf[1]) == 0
K1 = sp.simplify(cf[2] / den) if form_ok else None
c01 = sp.simplify(cf[0] / den) if form_ok else None
cs2_iii = sp.simplify(-c01 / (K1 * k**2)) if form_ok else None
rep.check("step (iii): one field is left, M_red = K (omega^2 - c_s^2 k^2) (polynomial of degree 2 in omega, even)",
          form_ok, f"K = {K1}, c_s^2 = {cs2_iii}", kind="method check")
R["K_M1"], R["cs2_M1_reduced"] = str(K1), str(cs2_iii)
ok_iii = form_ok and zero_exact(cs2_iii - HEAD, {gt: SAMP[gt], k: SAMP[k], Mp2: SAMP[Mp2]})[0]
rep.check("H-a (M1 step iii, reduced action): c_s^2 = gt/(2 - 3 gt) exactly", ok_iii, cs2_iii)
ratio = sp.simplify(K1 / (-(2 - 3 * gt) / gt)) if form_ok else None
ratio_ok = form_ok and (not ratio.has(gt)) and bool(ratio.is_positive)
rep.check("H-b (M1 step iii): K = -(2 - 3 gt)/gt times a positive factor", ratio_ok, f"K / (-(2-3gt)/gt) = {ratio}")
R["K_ratio_M1"] = str(ratio)

# ------------------------------------------------------------------ 6. H-c windows (M1)
rep.p("\n== 6. H-c: windows solved exactly as sets in gt (M1: K and c_s^2 from step iii)")
Re = sp.S.Reals
if form_ok:
    Kg = sp.simplify(K1.subs({Mp2: 1, k: 1}))
    cg = sp.simplify(cs2_iii)
    ghost = sp.Intersection(sp.solveset(Kg < 0, gt, Re), sp.solveset(cg > 0, gt, Re))
    grad = sp.Intersection(sp.solveset(Kg > 0, gt, Re), sp.solveset(cg < 0, gt, Re))
    healthy = sp.Intersection(sp.solveset(Kg > 0, gt, Re), sp.solveset(cg > 0, gt, Re))
    superl = sp.solveset(cg > 1, gt, Re)
else:
    ghost = grad = healthy = superl = None
exp_ghost = sp.Interval.open(0, sp.Rational(2, 3))
exp_grad = sp.Union(sp.Interval.open(-sp.oo, 0), sp.Interval.open(sp.Rational(2, 3), sp.oo))
rep.check("H-c (M1): ghost set (K < 0, c_s^2 > 0) is exactly 0 < gt < 2/3", ghost == exp_ghost, ghost)
rep.check("H-c (M1): gradient-unstable set (K > 0, c_s^2 < 0) is exactly gt < 0 or gt > 2/3", grad == exp_grad, grad)
rep.check("H-c (M1): ghost-free and gradient-stable set is empty", healthy == sp.S.EmptySet, healthy)
if form_ok:
    lim0p, lim0m = sp.limit(Kg, gt, 0, "+"), sp.limit(Kg, gt, 0, "-")
    K23 = sp.simplify(Kg.subs(gt, sp.Rational(2, 3)))
    c23p, c23m = sp.limit(cg, gt, sp.Rational(2, 3), "+"), sp.limit(cg, gt, sp.Rational(2, 3), "-")
    ends = (abs(lim0p) == sp.oo and abs(lim0m) == sp.oo and K23 == 0 and abs(c23p) == sp.oo and abs(c23m) == sp.oo)
    ends_d = f"K(gt->0+) = {lim0p}, K(gt->0-) = {lim0m}, K(2/3) = {K23}, c_s^2(2/3+) = {c23p}, c_s^2(2/3-) = {c23m}"
else:
    ends, ends_d = False, "no reduced form"
rep.check("H-c (M1) end points: K diverges at gt -> 0; K = 0 and c_s^2 has a pole at gt = 2/3", ends, ends_d)
rep.p(f"   reported: superluminal set c_s^2 > 1 is {superl}")
R["windows_M1"] = {"ghost": str(ghost), "gradient": str(grad), "healthy": str(healthy), "superluminal": str(superl)}

# ------------------------------------------------------------------ 7. C0: GR alone
rep.p("\n== 7. C0: GR alone (phi, lambda, V, gamma removed)")
og = C.expand_action("mink", 0, mimetic=False, log=rep.p)
Fg = og["fields"]
ord0 = ["Phi", "B", "Psi", "E", "h"]
M0 = C.fourier_matrix(og["L2"], [Fg[n] for n in ord0])
MN0 = sub(M0, ["Phi", "Psi"], ord0)
det0 = sp.factor(MN0.det())
rep.p(f"   GR scalar det (Newtonian gauge) = {det0}")
rep.check("C0: GR scalar sector has no propagating mode (gauge-fixed det has no root in omega)",
          (not det0.has(w)) and sp.simplify(det0) != 0, det0, kind="control")
Mhh0 = sp.expand(M0[ord0.index("h"), ord0.index("h")])
cT = sp.Poly(Mhh0, w).all_coeffs()[::-1]
cT_ok = len(cT) == 3 and sp.simplify(cT[1]) == 0 and sp.simplify(-cT[0] / (cT[2] * k**2)) == 1 and bool(cT[2].is_positive)
rep.check("C0: GR tensor mode has omega^2 = k^2 and positive energy (coefficient of omega^2 > 0)", cT_ok,
          f"M_hh = {sp.factor(Mhh0)}", kind="control")

# ------------------------------------------------------------------ 8. C1: gt = 0
rep.p("\n== 8. C1: the higher-derivative term off (gt = 0): pure mimetic dust")
c1_ok = True
for nm, Mx in (("unitary", MU), ("Newtonian", MN)):
    d0 = sp.factor(sp.expand(Mx.subs(gt, 0).det(method="berkowitz")))
    m0, P0 = C.poly_in_w(d0)
    ok = (P0 is not None) and P0.degree() == 0
    rep.p(f"   gt = 0, {nm} det = {d0}  (zero-root multiplicity {m0})")
    c1_ok &= ok
rep.check("C1 (M1): at gt = 0 every root of the det is omega = 0 (no wave, c_s^2 = 0), both gauges", c1_ok,
          kind="control")

# ------------------------------------------------------------------ 9. C4 and the numeric Krein machinery
rep.p("\n== 9. C4: canonical scalar L = -(s/2)(d chi)^2 through the same Fourier and Krein code")


def krein_np(Mf, dMf, w0, args, tol=1e-9):
    Mv = np.array(Mf(w0, *args), dtype=complex)
    _, sv, Vh = np.linalg.svd(Mv)
    # Frozen zero test: below tol x the largest singular value.  Known defect (found by control C4 on the first
    # main run, kept and disclosed): for a 1x1 matrix the only singular value is also the largest, so a numerically
    # computed root is never 'zero'.  Multi-field matrices (the 7x7 physics matrix) are not affected.
    null = np.where(sv < tol * sv[0])[0]
    N = Vh.conj().T[:, null]
    dMv = np.array(dMf(w0, *args), dtype=complex)
    Q = N.conj().T @ dMv @ N
    Q = (Q + Q.conj().T) / 2
    ev = np.linalg.eigvalsh(Q) if Q.size else np.array([])
    big = float(np.max(np.abs(ev))) if ev.size else 0.0
    nz = [e for e in ev if big > 0 and abs(e) >= tol * big]
    sign = int(np.sign(nz[0]) * np.sign(w0)) if len(nz) == 1 else None
    return {"null_dim": int(len(null)), "sv_small": [float(s_) for s_ in sv[-4:]], "q_eigs": [float(e) for e in ev],
            "n_nonzero": len(nz), "sign": sign}


def krein_mp(Mf, dMf, w0, args, tol=mp.mpf("1e-35")):
    Mv = mp.matrix(Mf(w0, *args))
    U, S, V = mp.svd_c(Mv)
    svals = [S[i] for i in range(len(S))]
    smax = max(abs(s_) for s_ in svals)
    null = [i for i, s_ in enumerate(svals) if abs(s_) < tol * smax]
    n = Mv.rows
    N = mp.matrix(n, len(null))
    for j, i in enumerate(null):
        for r_ in range(n):
            N[r_, j] = mp.conj(V[i, r_])
    dMv = mp.matrix(dMf(w0, *args))
    Q = N.H * dMv * N
    Q = (Q + Q.H) * mp.mpf("0.5")
    ev, _ = mp.eighe(Q) if len(null) else ([], None)
    ev = [ev[i] for i in range(len(ev))] if len(null) else []
    big = max(abs(e) for e in ev) if ev else mp.mpf(0)
    nz = [e for e in ev if big > 0 and abs(e) >= tol * big]
    sign = int(mp.sign(nz[0]) * mp.sign(w0)) if len(nz) == 1 else None
    return {"null_dim": len(null), "sv_small": [mp.nstr(s_, 5) for s_ in sorted(svals, key=abs)[:4]],
            "q_eigs": [mp.nstr(e, 8) for e in ev], "n_nonzero": len(nz), "sign": sign}


chi = sp.Function("chi", real=True)(t, x)
c4_ok = True
for s_ in (1, -1):
    L2c = sp.Rational(s_, 2) * (sp.diff(chi, t)**2 - sp.diff(chi, x)**2)
    Mc = C.fourier_matrix(L2c, [chi])
    Pc = sp.Poly(Mc[0, 0].subs(k, 1), w)
    roots = np.roots([complex(c_) for c_ in Pc.all_coeffs()])
    Mf = sp.lambdify((w, k), Mc, "numpy")
    dMf = sp.lambdify((w, k), Mc.diff(w), "numpy")
    kr = [krein_np(Mf, dMf, float(np.real(r_)), (1.0,)) for r_ in roots]
    ok = np.allclose(sorted(np.real(roots)), [-1, 1]) and all(q["sign"] == s_ for q in kr)
    rep.p(f"   s = {s_:+d}: M = {Mc[0, 0]}, roots {np.round(roots, 12)}, Krein signs {[q['sign'] for q in kr]}")
    c4_ok &= bool(ok)
rep.check("C4: canonical scalar gives omega^2 = k^2 and energy sign s for s = +1 and -1", c4_ok, kind="control")

# POST-HOC C4b (added after the first main run; NOT a frozen control; does not enter the exit code).
# The same canonical scalar plus a decoupled algebraic field mu, L = -(s/2)(d chi)^2 + mu^2/2, so that the matrix
# has a second singular value that sets the scale of the frozen zero test.
mu_ = sp.Function("mu", real=True)(t, x)
c4b = []
for s_ in (1, -1):
    L2c = sp.Rational(s_, 2) * (sp.diff(chi, t)**2 - sp.diff(chi, x)**2) + mu_**2 / 2
    Mc = C.fourier_matrix(L2c, [chi, mu_])
    Pc = sp.Poly(Mc[0, 0].subs(k, 1), w)
    roots = np.roots([complex(c_) for c_ in Pc.all_coeffs()])
    Mf = sp.lambdify((w, k), Mc, "numpy")
    dMf = sp.lambdify((w, k), Mc.diff(w), "numpy")
    kr = [krein_np(Mf, dMf, float(np.real(r_)), (1.0,)) for r_ in roots]
    c4b.append({"s": s_, "roots": [str(r_) for r_ in roots], "signs": [q["sign"] for q in kr]})
    rep.p(f"   POST-HOC C4b (not counted): s = {s_:+d} with a decoupled algebraic field: roots {np.round(roots, 12)}, "
          f"Krein signs {[q['sign'] for q in kr]} (expected {s_:+d})")
R["POSTHOC_C4b"] = c4b

# ------------------------------------------------------------------ 10. N1 numerics
rep.p("\n== 10. N1: numerical confirmation from the brute-force matrix (closed form not used)")
GT_LIST = [(sp.Integer(-1), "-1"), (sp.Rational(-1, 5), "-0.2"), (sp.Rational(-1, 100), "-0.01"),
           (sp.Rational(85, 10**12), "8.5e-11"), (sp.Rational(1, 100), "0.01"), (sp.Rational(1, 5), "0.2"),
           (sp.Rational(2, 5), "0.4"), (sp.Rational(11, 20), "0.55"), (sp.Rational(13, 20), "0.65"),
           (sp.Rational(7, 10), "0.7"), (sp.Integer(1), "1"), (sp.Integer(3), "3")]
K_LIST = [sp.Rational(1, 2), sp.Integer(2)]
Mfn = sp.lambdify((w, k, gt, Mp2), M, "numpy")
dMfn = sp.lambdify((w, k, gt, Mp2), M.diff(w), "numpy")
Mfm = sp.lambdify((w, k, gt, Mp2), M, "mpmath")
dMfm = sp.lambdify((w, k, gt, Mp2), M.diff(w), "mpmath")
MhhS = sp.expand(M[iH, iH])
n1_rows, n1_ok, sign_agree = [], True, True
for gv_, glab in GT_LIST:
    use_mp = glab == "8.5e-11"
    for kv in K_LIST:
        row = {"gt": glab, "k": str(kv), "precision": "mpmath 50 digits" if use_mp else "numpy double"}
        dU = sp.expand(MU.subs({gt: gv_, k: kv, Mp2: 1}).det(method="berkowitz"))
        m_, P_ = C.poly_in_w(dU)
        coeffs = P_.all_coeffs()
        form_val = gv_ / (2 - 3 * gv_)
        if use_mp:
            mp.mp.dps = 50
            roots = mp.polyroots([mp.mpf(sp.Rational(c_).p) / mp.mpf(sp.Rational(c_).q) for c_ in coeffs],
                                 maxsteps=500, extraprec=200)
            tol = mp.mpf("1e-30")
        else:
            roots = np.roots([complex(c_) for c_ in coeffs])
            tol = 1e-8
        row["zero_root_multiplicity"] = m_
        row["roots"] = [str(r_) for r_ in roots]
        pt_ok = len(roots) == 2
        for r_ in roots:
            re_, im_ = (r_.real, r_.imag) if not use_mp else (mp.re(r_), mp.im(r_))
            mag = abs(r_)
            if abs(im_) < 1e-9 * mag:            # real root
                val = (re_ / float(kv))**2 if not use_mp else (re_ / mp.mpf(kv))**2
                ref = float(form_val) if not use_mp else mp.mpf(form_val.p) / mp.mpf(form_val.q)
                err = abs(val / ref - 1) if ref != 0 else abs(val)
                if use_mp:
                    kr = krein_mp(Mfm, dMfm, re_, (mp.mpf(kv), mp.mpf(gv_.p) / mp.mpf(gv_.q), mp.mpf(1)))
                else:
                    kr = krein_np(Mfn, dMfn, float(re_), (float(kv), float(gv_), 1.0))
                expect_sign = -1 if 0 < gv_ < sp.Rational(2, 3) else None
                Ksign = int(sp.sign(K1.subs({gt: gv_, k: kv, Mp2: 1}))) if form_ok else None
                ok = (err < tol and kr["null_dim"] == 3 and kr["n_nonzero"] == 1
                      and (expect_sign is None or kr["sign"] == expect_sign))
                sign_agree &= (kr["sign"] == Ksign)
                row.setdefault("real_roots", []).append(
                    {"omega": str(re_), "omega2_over_k2": str(val), "rel_err_vs_formula": str(err),
                     "krein": kr, "sign_K_step_iii": Ksign})
            elif abs(re_) < 1e-9 * mag:          # imaginary root: gradient instability
                val = abs(im_) / (float(kv) if not use_mp else mp.mpf(kv))
                ref = abs(float(form_val))**0.5 if not use_mp else mp.sqrt(abs(mp.mpf(form_val.p) / mp.mpf(form_val.q)))
                err = abs(val / ref - 1)
                ok = err < tol and form_val < 0
                row.setdefault("imag_roots", []).append({"growth_rate_over_k": str(val), "rel_err_vs_formula": str(err)})
            else:
                ok = False
                row.setdefault("complex_roots", []).append(str(r_))
            pt_ok &= bool(ok)
        # tensor mode at this point
        Ph = sp.Poly(MhhS.subs({gt: gv_, k: kv, Mp2: 1}), w)
        troots = np.roots([complex(c_) for c_ in Ph.all_coeffs()])
        tk = [krein_np(Mfn, dMfn, float(np.real(r_)), (float(kv), float(gv_), 1.0)) for r_ in troots]
        t_ok = (np.allclose(np.sort(np.real(troots)), [-float(kv), float(kv)], rtol=1e-10)
                and all(q["sign"] == 1 and q["n_nonzero"] == 1 for q in tk))
        row["tensor"] = {"roots": [str(r_) for r_ in troots], "krein_signs": [q["sign"] for q in tk]}
        pt_ok &= bool(t_ok)
        row["pass"] = bool(pt_ok)
        n1_ok &= bool(pt_ok)
        n1_rows.append(row)
        rr = row.get("real_roots", [])
        ir = row.get("imag_roots", [])
        rep.p(f"   gt = {glab:>8}, k = {str(kv):>3}: "
              + (f"real roots, omega^2/k^2 = {rr[0]['omega2_over_k2'][:22]} (rel err {float(rr[0]['rel_err_vs_formula']):.1e}), "
                 f"null dim {rr[0]['krein']['null_dim']}, nonzero {rr[0]['krein']['n_nonzero']}, "
                 f"Krein signs {[q['krein']['sign'] for q in rr]}" if rr else "")
              + (f"imaginary roots, |Im omega|/k = {ir[0]['growth_rate_over_k'][:22]} (rel err {float(ir[0]['rel_err_vs_formula']):.1e})" if ir else "")
              + (f" COMPLEX {row['complex_roots']}" if row.get("complex_roots") else "")
              + f"; tensor Krein {row['tensor']['krein_signs']}; {'ok' if pt_ok else 'FAIL'}")
R["N1"] = n1_rows
rep.check("N1: roots match gt/(2 - 3 gt) (real: omega^2/k^2; imaginary: |Im omega|/k), 3-dim null space, one nonzero "
          "restricted eigenvalue, negative sign for 0 < gt < 2/3, tensor omega^2 = k^2 with positive sign, all 24 points",
          n1_ok, kind="pass line (N1)")
rep.check("H-b (M1 step iv): the gauge-invariant (Krein) sign equals sign(K) of step (iii) at every real root in N1",
          sign_agree and form_ok, kind="pass line")

# G2 pair row (reported): gt_max = 8.5e-11 printed, c_s^2,max = 4.2e-11 printed
lo_g, hi_g = sp.Rational(845, 10**13), sp.Rational(855, 10**13)
lo_c, hi_c = sp.Rational(415, 10**13), sp.Rational(425, 10**13)
f_ = sp.Lambda(gt, gt / (2 - 3 * gt))
consistent = f_(lo_g) < hi_c and f_(hi_g) >= lo_c   # monotone increasing near 0
rep.p(f"   reported row: CFG124's G2 pair (gt_max 8.5e-11, c_s^2,max 4.2e-11): formula at 8.5e-11 gives "
      f"{sp.N(f_(sp.Rational(85, 10**12)), 12)}; a gt in [8.45e-11, 8.55e-11) giving c_s^2 in [4.15e-11, 4.25e-11) "
      f"exists: {bool(consistent)}")
R["G2_pair_consistent_at_printed_precision"] = bool(consistent)

rc = rep.finish()
sys.exit(rc)
