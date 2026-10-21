"""AG6C gate (iv): health of candidate C1 across 1e-4 .. 1e4 a0, plus C2's kinetic structure and L49 read literally.

Criteria: FROZEN_CRITERIA.md (committed alone first, e926935c3).
Dark sector (units K = 1, a0 = 1): l(X) = sgn(X)[s - ln(1+s)], s = sqrt(2|X|), X = (E^2 - B^2)/2;
  D = l_X E, H = l_X B;  dD = l_X dE + l_XX E (E.dE - B.dB),  dH = l_X dB + l_XX B (E.dE - B.dB).
H1/H2 sympy; H3 NLED plane waves on random (E, B) backgrounds; H3b (disclosed addition, not frozen) near-null backgrounds;
H4 dust + NLED + Newtonian gravity linear system about static electric backgrounds; H5 C2 (Blanchet-Le Tiec NR reduction);
H6 L49 with inertia rho_c; causality A/B table.
Run: python3 ag6c_gate_iv.py   (AG6C_MUTATE=a|b|c|d: wrong-sign dark kinetic | l = X - X^2 beyond X = 1/6 |
                                q^2 = 0.99 | rho < 0; each must be flagged)
"""
import json
import math
import os
import sys
import time

import numpy as np
import sympy as sp

MODE = os.environ.get("AG6C_MUTATE", "")
assert MODE in ("", "a", "b", "c", "d")
HERE = os.path.dirname(os.path.abspath(__file__))
SUF = f"_MUTATE_{MODE}" if MODE else ""
OUT = open(os.path.join(HERE, f"ag6c_gate_iv{SUF}.out"), "w")
RES = {"lane": "AG6C", "script": "ag6c_gate_iv", "mutate": MODE, "checks": {}, "numbers": {}}
FAILS = []
T0 = time.time()
rng = np.random.default_rng(20261020)


def P(*a):
    s = " ".join(str(x) for x in a)
    print(s, flush=True)
    OUT.write(s + "\n")


def check(name, ok, detail):
    P(f"  [{'PASS' if ok else 'FAIL'}] {name}: {detail}")
    RES["checks"][name] = dict(ok=bool(ok), detail=detail)
    if not ok:
        FAILS.append(name)


def lX_lXX(X):
    """C1's dark Lagrangian derivatives (both branches); MUTATE a flips the sign; MUTATE b uses l = X - X^2."""
    if MODE == "b":
        return 1 - 2 * X, -2.0
    s = math.sqrt(2 * abs(X))
    lx = 1 / (1 + s)
    if s == 0:
        lxx = -math.inf if X >= 0 else math.inf
    else:
        lxx = (-1 if X > 0 else 1) / ((1 + s) ** 2 * s)
    if MODE == "a":
        return -lx, -lxx
    return lx, lxx


P("AG6C gate (iv): health of C1" + (f"  [MUTATE {MODE}]" if MODE else ""))

# ================================================================== H1 / H2 (sympy)
P("\nH1/H2  sympy: l_X and l_X + 2 X l_XX on both branches (s = sqrt(2|X|))")
s_ = sp.symbols("s", positive=True)
Xp = s_ ** 2 / 2
Xs = sp.symbols("X", real=True)
l_plus = sp.sqrt(2 * Xs) - sp.log(1 + sp.sqrt(2 * Xs))
l_minus = -(sp.sqrt(-2 * Xs) - sp.log(1 + sp.sqrt(-2 * Xs)))
res_h = {}
for name, lf, sub in (("electric X>0", l_plus, Xp), ("magnetic X<0", l_minus, -Xp)):
    lx = sp.simplify(sp.diff(lf, Xs).subs(Xs, sub))
    hyp = sp.simplify((sp.diff(lf, Xs) + 2 * Xs * sp.diff(lf, Xs, 2)).subs(Xs, sub))
    res_h[name] = (lx, hyp)
    P(f"  {name}: l_X = {lx},  l_X + 2X l_XX = {hyp}")
h1 = all(sp.simplify(v[0] - 1 / (1 + s_)) == 0 for v in res_h.values())
h2 = all(sp.simplify(v[1] - 1 / (1 + s_) ** 2) == 0 for v in res_h.values())
check("H1 kinetic positivity (dark sector)", h1, "l_X = 1/(1+s) > 0 on both branches; dust kinetic rho|v|^2/2 > 0 for rho > 0; "
      "graviton = GR")
check("H2 hyperbolicity coefficient", h2, "l_X + 2X l_XX = 1/(1+s)^2 > 0 on both branches")
P("  Forced structure: on a pure electric background l(E^2/2) must equal the Legendre dual of W_full, whose cubic term is")
P("  (2X)^(3/2)/3; the only Lorentz invariants are X and Y = E.B, and both vanish on every NULL field, so any Lorentz-")
P("  invariant l(X, Y) carrying the simple-mu tether is non-analytic on the whole null cone X = Y = 0 (l_XX ~ |X|^-1/2).")


# ================================================================== H3 NLED dispersion (quadratic eigenproblem)
def cross_mat(k):
    return np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])


def nled_omegas(E, B, k):
    X = 0.5 * (E @ E - B @ B)
    lx, lxx = lX_lXX(X)
    Kx = cross_mat(k)
    M2 = lx * np.eye(3) + lxx * np.outer(E, E)
    M1 = lxx * (Kx @ np.outer(B, E) - np.outer(E, B) @ Kx)
    M0 = lx * Kx @ Kx - lxx * Kx @ np.outer(B, B) @ Kx
    try:
        Minv = np.linalg.inv(M2)
    except np.linalg.LinAlgError:            # only reachable in MUTATE b (l = X - X^2), where H3 is not evaluated
        return np.full(6, 1j)
    Cmp = np.block([[np.zeros((3, 3)), np.eye(3)], [-Minv @ M0, -Minv @ M1]])
    return np.linalg.eigvals(Cmp)


P("\nH3  NLED plane waves on 2000 random (E, B) backgrounds, |E|, |B| log-uniform in [1e-4, 1e4] a0, random directions")


def rand_unit():
    v = rng.normal(size=3)
    return v / np.linalg.norm(v)


worst3 = 0.0
nbad3 = 0
for _ in range(2000):
    Em, Bm = 10 ** rng.uniform(-4, 4), 10 ** rng.uniform(-4, 4)
    E, B, k = Em * rand_unit(), Bm * rand_unit(), rand_unit()
    w = nled_omegas(E, B, k)
    sc = np.max(np.abs(w))
    r = np.max(np.abs(w.imag)) / sc
    worst3 = max(worst3, r)
    nbad3 += r > 1e-8
# pure electric: extraordinary speed check v^2 = cos^2(th) + (1 + e) sin^2(th)
maxdev = 0.0
for e in (1e-4, 1e-2, 1.0, 1e2, 1e4):
    for th in (0.3, 0.9, math.pi / 2):
        k = np.array([math.sin(th), 0, math.cos(th)])
        w = np.sort(np.abs(nled_omegas(np.array([0, 0, e]), np.zeros(3), k).real))
        vex = math.sqrt(math.cos(th) ** 2 + (1 + e) * math.sin(th) ** 2)
        if MODE in ("", "c", "d"):
            maxdev = max(maxdev, abs(w[-1] / vex - 1), abs(w[-3] - 1))
P(f"  max |Im omega|/max|omega| over 2000 backgrounds: {worst3:.2e} ({nbad3} backgrounds above 1e-8)")
_r3 = []
rng_r = np.random.default_rng(20261020)
for _ in range(2000):
    Em, Bm = 10 ** rng_r.uniform(-4, 4), 10 ** rng_r.uniform(-4, 4)
    v1 = rng_r.normal(size=3); v2 = rng_r.normal(size=3); v3 = rng_r.normal(size=3)
    w = nled_omegas(Em * v1 / np.linalg.norm(v1), Bm * v2 / np.linalg.norm(v2), v3 / np.linalg.norm(v3))
    _r3.append(np.max(np.abs(w.imag)) / np.max(np.abs(w)))
_r3 = np.array(_r3)
P(f"  counts above 1e-8 / 1e-6 / 1e-3 / 1e-1: {(_r3 > 1e-8).sum()} / {(_r3 > 1e-6).sum()} / {(_r3 > 1e-3).sum()} / {(_r3 > 1e-1).sum()}"
  f"  (the machinery's noise floor is ~1e-8, see K-H3)")
RES["numbers"]["H3_counts"] = {t: int((_r3 > t).sum()) for t in (1e-8, 1e-6, 1e-3, 1e-1)}
P(f"  pure electric: modes = {{1 (ordinary), sqrt(cos^2 + (1+e) sin^2) (extraordinary)}}: max deviation {maxdev:.1e}")
RES["numbers"]["H3"] = dict(max_imag_ratio=worst3, n_bad=int(nbad3), extraordinary_dev=maxdev)
if MODE in ("", "c", "d"):
    check("H3 NLED dispersion real (random backgrounds)", worst3 <= 1e-8 and maxdev <= 1e-8,
          f"max |Im w|/|w| {worst3:.1e}; extraordinary v^2 = 1 + e sin^2 to {maxdev:.0e}")

# ------------------------------------------------------------------ H3 controls + diagnosis (disclosed additions)
if MODE == "":
    P("\nH3 controls (disclosed addition): the same eigen-machinery on Maxwell and on a causal L = X + 0.1 X^2")
    saved = lX_lXX

    def run_ctrl(fun, nmax, Fmax):
        worst = 0.0
        for _ in range(nmax):
            E, B, k = 10 ** rng.uniform(-4, math.log10(Fmax)) * rand_unit(), 10 ** rng.uniform(-4, math.log10(Fmax)) * rand_unit(), rand_unit()
            X = 0.5 * (E @ E - B @ B)
            lx, lxx = fun(X)
            Kx = cross_mat(k)
            M2 = lx * np.eye(3) + lxx * np.outer(E, E)
            M1 = lxx * (Kx @ np.outer(B, E) - np.outer(E, B) @ Kx)
            M0 = lx * Kx @ Kx - lxx * Kx @ np.outer(B, B) @ Kx
            Cmp = np.block([[np.zeros((3, 3)), np.eye(3)], [-np.linalg.inv(M2) @ M0, -np.linalg.inv(M2) @ M1]])
            w = np.linalg.eigvals(Cmp)
            worst = max(worst, np.max(np.abs(w.imag)) / np.max(np.abs(w)))
        return worst
    wmax = run_ctrl(lambda X: (1.0, 0.0), 500, 1e4)
    wcau = run_ctrl(lambda X: (1 + 0.2 * X, 0.2), 500, 1.0)
    P(f"  Maxwell: max |Im w|/|w| = {wmax:.1e};  L = X + 0.1 X^2 (|E|, |B| <= 1, l_XX > 0): {wcau:.1e}")
    # first run used 1e-8 here and 'failed' at 6.4e-9/1.5e-8: that is the companion-matrix noise floor over 8 decades of field,
    # not a physical root; the control line is 1e-6 (disclosed). Genuine H3 failures sit at 1e-3..1.
    check("K-H3 machinery control", wmax <= 1e-6 and wcau <= 1e-6,
          "real frequencies (to the 1e-8 noise floor) for Maxwell and for a causal L(X)")
    RES["numbers"]["H3_controls"] = dict(maxwell=wmax, causal=wcau)

    P("\nH3c (disclosed addition): diagnose every failing H3 background in the field's own rest frame (E' || B')")
    rng2 = np.random.default_rng(20261020)          # replay the frozen H3 draws
    nfail, n_xpos, n_rest_ok, worst_rest, betas, hess_flags = 0, 0, 0, 0.0, [], []
    for _ in range(2000):
        Em, Bm = 10 ** rng2.uniform(-4, 4), 10 ** rng2.uniform(-4, 4)
        v1 = rng2.normal(size=3); v2 = rng2.normal(size=3); v3 = rng2.normal(size=3)
        E, B, k = Em * v1 / np.linalg.norm(v1), Bm * v2 / np.linalg.norm(v2), v3 / np.linalg.norm(v3)
        w = nled_omegas(E, B, k)
        if np.max(np.abs(w.imag)) / np.max(np.abs(w)) <= 1e-6:      # above the 1e-8 noise floor (K-H3)
            continue
        nfail += 1
        X = 0.5 * (E @ E - B @ B)
        n_xpos += X > 0
        S = np.cross(E, B)
        Sm = np.linalg.norm(S)
        U = E @ E + B @ B
        beta = (U - math.sqrt(max(U * U - 4 * Sm * Sm, 0.0))) / (2 * Sm) if Sm > 0 else 0.0
        nh = S / Sm if Sm > 0 else np.array([1.0, 0, 0])
        gam = 1 / math.sqrt(1 - beta * beta)
        Epar, Bpar = (E @ nh) * nh, (B @ nh) * nh
        Ep = Epar + gam * (E - Epar + beta * np.cross(nh, B))
        Bp = Bpar + gam * (B - Bpar - beta * np.cross(nh, E))
        wr = 0.0
        for _ in range(100):
            wq = nled_omegas(Ep, Bp, rand_unit())
            wr = max(wr, np.max(np.abs(wq.imag)) / np.max(np.abs(wq)))
        worst_rest = max(worst_rest, wr)
        n_rest_ok += wr <= 1e-6
        ep = math.sqrt(2 * abs(0.5 * (Ep @ Ep - Bp @ Bp)))
        betas.append(beta * math.sqrt(1 + ep))
        # Hessian of l in (E'_z, B'_z) along the common direction: l_EE = l_X + l_XX E'^2, l_BB = -l_X + l_XX B'^2.
        # Well-posed (electric-like E, magnetic-like B) needs l_EE > 0 and l_BB < 0; analytic form: B'^2 < s (X > 0),
        # E'^2 < s (X < 0), s = sqrt(2|X|) in a0 units.
        Xp_ = 0.5 * (Ep @ Ep - Bp @ Bp)
        lx_, lxx_ = lX_lXX(Xp_)
        lEE, lBB = lx_ + lxx_ * (Ep @ Ep), -lx_ + lxx_ * (Bp @ Bp)
        sp_ = math.sqrt(2 * abs(Xp_))
        flip = not (lEE > 0 and lBB < 0)
        pred = (Bp @ Bp >= sp_) if Xp_ > 0 else (Ep @ Ep >= sp_)
        hess_flags.append((flip, pred, wr > 1e-6))
    P(f"  genuinely failing backgrounds (|Im w|/|w| > 1e-6): {nfail}; with X > 0 (electric-dominated): {n_xpos}; real in their "
      f"own rest frame (lab-time tipping only, criterion-B type): {n_rest_ok}; complex in every frame: {nfail - n_rest_ok}")
    if betas:
        P(f"  drift speed x rest-frame superluminal speed, beta*sqrt(1 + e'): min {min(betas):.3f}, median {np.median(betas):.3f}"
          f"  (the superluminal cone tips over the lab-time slices when this exceeds ~1)")
    hf = np.array(hess_flags, dtype=bool) if hess_flags else np.zeros((0, 3), bool)
    agree = int(np.sum(hf[:, 0] == hf[:, 2])) if len(hf) else 0
    agree2 = int(np.sum(hf[:, 1] == hf[:, 2])) if len(hf) else 0
    P(f"  rest-frame Hessian of l in (E', B') has the wrong signature in {int(hf[:, 0].sum()) if len(hf) else 0} of {nfail}; it matches "
      f"rest-frame complex roots in {agree}/{nfail}; analytic line (subdominant parallel field)^2 >= sqrt(2|X|) predicts {agree2}/{nfail}")
    P("  reading: the wrong-signature backgrounds are ill-posed in EVERY frame (the dispersion is scale-free, so Im omega ~ |k|:")
    P("  a gradient instability); they need a strong dark field plus a comparable PARALLEL field of the other kind")
    P("  ((subdominant)^2 >= sqrt(2|X|) in a0 units). The rest are well posed in their own frame and fail only when the forced")
    P("  superluminal cone is boosted past the lab-time slices. A pure electric background (every static galaxy) meets neither.")
    RES["numbers"]["H3c_hessian"] = dict(n_wrong_signature=int(hf[:, 0].sum()) if len(hf) else 0, hessian_predicts=agree,
                                         analytic_predicts=agree2)
    RES["numbers"]["H3c"] = dict(n_fail=nfail, n_Xpos=int(n_xpos), n_rest_frame_real=int(n_rest_ok), worst_rest=worst_rest,
                                 beta_vs_min=min(betas) if betas else None, beta_vs_median=float(np.median(betas)) if betas else None)

# ------------------------------------------------------------------ H3b near-null backgrounds (disclosed addition)
if MODE == "":
    P("\nH3b (disclosed addition, not in the frozen list): near-null backgrounds |B| = |E|(1 - eta), E at angle psi to B")
    tabn = {}
    for Fm in (1e-4, 1e-2, 1.0, 1e2):
        for eta in (1e-1, 1e-2, 1e-4, 1e-6):
            for psi in (0.0, math.pi / 4, math.pi / 2):
                E = Fm * np.array([0, 0, 1.0])
                B = Fm * (1 - eta) * np.array([math.sin(psi), 0, math.cos(psi)])
                worst = 0.0
                for _ in range(200):
                    w = nled_omegas(E, B, rand_unit())
                    worst = max(worst, np.max(np.abs(w.imag)) / np.max(np.abs(w)))
                tabn[f"F{Fm:g}_eta{eta:g}_psi{psi:.2f}"] = worst
        row = "  ".join(f"eta {eta:g}: " + "/".join(f"{tabn[f'F{Fm:g}_eta{eta:g}_psi{p:.2f}']:.0e}"
                                                    for p in (0.0, math.pi / 4, math.pi / 2)) for eta in (1e-1, 1e-2, 1e-4, 1e-6))
        P(f"  |E| = {Fm:g} a0 -> max|Im w|/|w| (psi = 0/45/90 deg): {row}")
    nfail = sum(v > 1e-6 for v in tabn.values())          # above the 1e-8 noise floor (K-H3)
    RES["numbers"]["H3b"] = tabn
    P(f"  near-null cells with complex lab-frame frequencies (> 1e-6): {nfail} of {len(tabn)} (REPORTED; not a frozen check)")
    RES["H3b_near_null_failures"] = int(nfail)

# ================================================================== H4 coupled dust + NLED + gravity
P("\nH4  dust + NLED + Newtonian gravity about static electric backgrounds (units c = K = rho0 = a0 = 1)")


def h4_matrix(e, th, k, cs, q=1.0, rho0=1.0, gam_sign=1.0):
    X = 0.5 * e * e
    lx, lxx = lX_lXX(X)
    eps = np.diag([lx, lx, lx + 2 * X * lxx])
    epsinv = np.linalg.inv(eps)
    kv = k * np.array([math.sin(th), 0.0, math.cos(th)])
    Kx = cross_mat(kv)
    gam = gam_sign * cs * cs / abs(rho0)          # pressure: dv' = -i k gam drho  (p = gam rho^2 / 2)
    A = np.zeros((10, 10), dtype=complex)
    A[0, 1:4] = -1j * rho0 * kv                             # drho'
    A[1:4, 0] = 1j * kv / (k * k) - 1j * kv * gam           # gravity (K = 1) + pressure
    A[1:4, 4:7] = q * np.eye(3)                             # dark force per unit mass
    A[7:10, 4:7] = -1j * Kx                                 # dB' = -i k x dE
    A[4:7, 7:10] = epsinv @ (1j * lx * Kx)                  # dE' = eps^-1 (i l_X k x dB - q K rho0 dv)
    A[4:7, 1:4] = -q * rho0 * epsinv
    return A


es = np.logspace(-4, 4, 81)
ths = np.linspace(0, math.pi / 2, 13)
ks = np.logspace(-3, 6, 37)
cs_list = [1e-7, 1e-4]
q_used = math.sqrt(0.99) if MODE == "c" else 1.0
rho_used = -1.0 if MODE == "d" else 1.0
if MODE == "b":
    es_scan = np.array([0.7])           # l = X - X^2 at X = 0.245 > 1/6
else:
    es_scan = es
growth = np.zeros((len(es_scan), len(ths), len(ks), len(cs_list)))
for a, e in enumerate(es_scan):
    for b_, th in enumerate(ths):
        for c_, k in enumerate(ks):
            for d_, cs in enumerate(cs_list):
                lam = np.linalg.eigvals(h4_matrix(e, th, k, cs, q=q_used, rho0=rho_used))
                growth[a, b_, c_, d_] = np.max(lam.real) / max(np.max(np.abs(lam)), 1.0)
worst4 = float(np.max(growth))
P(f"  grid: e {len(es_scan)} x angle {len(ths)} x k {len(ks)} x c_s {len(cs_list)}; max Re(lambda)/max(|lambda|, w_p) = {worst4:.2e}")
RES["numbers"]["H4_max_growth_ratio"] = worst4

# energy positivity on the Gauss-constraint surface (ghost check, linear Hamiltonian)
def h4_energy_min(e, th, k, cs, q=1.0, rho0=1.0):
    """coefficients of the conserved linear energy on the Gauss surface (K = 1):
    E >= rho0|dv|^2/2 + [gam + (q^2/E_k - 1)/k^2]|drho|^2/2 + (eps-part of the free dE) + l_X |dB|^2/2,
    E_k = khat.eps.khat (Thomson minimum of the electrostatic energy for the free charge q drho)."""
    X = 0.5 * e * e
    lx, lxx = lX_lXX(X)
    eps = np.diag([lx, lx, lx + 2 * X * lxx])
    khat = np.array([math.sin(th), 0.0, math.cos(th)])
    gam = cs * cs / abs(rho0)
    Ek = khat @ eps @ khat
    e_comb = gam + (q * q / Ek - 1) / k ** 2
    return min(rho0, lx, float(np.min(np.linalg.eigvalsh(eps))), e_comb)


emin = min(h4_energy_min(e, th, k, cs, q=q_used, rho0=rho_used) for e in es_scan for th in ths for k in ks[::6] for cs in cs_list)
P(f"  min coefficient of the linear energy (dust KE, pressure, dark E and B energies, Gauss-tied longitudinal) = {emin:.3e}")
RES["numbers"]["H4_energy_min"] = emin
if MODE == "":
    check("H4 coupled linear health (static electric backgrounds, 1e-4..1e4 a0)", worst4 <= 1e-7 and emin > 0,
          f"no growing mode anywhere on the grid ({worst4:.1e}); linear energy positive-definite (min coefficient {emin:.2e})")
    # longitudinal margin in deep MOND (the PAPER8 trap): omega^2 = K rho (1/E_k - 1) + c_s^2 k^2
    for e in (1e-4, 1e-2, 1.0):
        Ek_par = 1 / (1 + e) ** 2
        P(f"    e = {e:g}: longitudinal restoring along E: K rho (1/E_k - 1) = {1 / Ek_par - 1:.3e} (>= 0; -> 0 as e -> 0, "
          f"neutral, not unstable)")
else:
    # classify: growth at the largest k vs the middle of the k range (gradient-class grows with k; Jeans-class is bounded)
    gk = np.max(growth, axis=(0, 1, 3))
    absg = []
    for k in ks:
        lam_all = [np.max(np.linalg.eigvals(h4_matrix(e, th, k, cs_list[-1], q=q_used, rho0=rho_used)).real)
                   for e in es_scan[:: max(1, len(es_scan) // 9)] for th in ths[::3]]
        absg.append(max(lam_all))
    absg = np.array(absg)
    # classify in the deepest-MOND background of the scan (e = es_scan[0]) with the larger c_s: gradient-class growth
    # scales ~k at large k (a k-independent plasma/Jeans growth at large e would otherwise mask it; first MUTATE-d run)
    def gr(k):
        return max(np.max(np.linalg.eigvals(h4_matrix(es_scan[0], th, k, cs_list[-1], q=q_used, rho0=rho_used)).real)
                   for th in ths)
    g_hi, g_lo = gr(ks[-1]), gr(ks[-1] / 10)
    cls = "gradient-class (growth rises with k)" if (g_hi > 1e-6 and g_hi > 5 * max(g_lo, 1e-30)) else \
        ("Jeans-class (bounded, small k)" if absg.max() > 1e-6 else "none")
    P(f"  deepest background e = {es_scan[0]:g}: growth at k = 1e5 / 1e6: {g_lo:.3e} / {g_hi:.3e}")
    P(f"  MUTATE {MODE}: max growth rate {absg.max():.3e} w_p; at k = 1e6: {absg[-1]:.3e}; class: {cls}")
    RES["numbers"]["mutate_class"] = cls
    flagged = (worst4 > 1e-3) or (emin <= 0)
    want = {"a": "flag", "b": "gradient", "c": "Jeans", "d": "gradient"}[MODE]
    ok_class = (want == "flag") or (want == "gradient" and cls.startswith("gradient")) or (want == "Jeans" and cls.startswith("Jeans"))
    P(f"  tooth {'bites' if (flagged and ok_class) else 'DID NOT BITE'} (flagged {flagged}, class wanted {want})")
    FAILS.append(f"MUTATE {MODE}: flagged={flagged}, class={cls} (designed exit 1)")

# ================================================================== H5 C2 (Blanchet-Le Tiec NR reduction)
if MODE == "":
    P("\nH5  C2: NR reduction of sqrt(-g) J_mu Dxi^mu/dtau = -Pi_mu a^mu (+ total derivative) -> per element")
    P("    L = sigma v^2/2 + dPi/dt . v - sigma Phi - Pi.grad Phi - W(Pi)   (one Cartesian component shown)")
    sig, v, pdot, px, pp, Vv = sp.symbols("sigma v Pidot p_x p_Pi V", real=True)
    Lk = sig * v ** 2 / 2 + pdot * v
    Hess = sp.Matrix([[sp.diff(Lk, a, b) for b in (v, pdot)] for a in (v, pdot)])
    ev = list(Hess.eigenvals().keys())
    sol = sp.solve([sp.Eq(px, sp.diff(Lk, v)), sp.Eq(pp, sp.diff(Lk, pdot))], [v, pdot], dict=True)[0]
    Hm = sp.simplify((px * v + pp * pdot - Lk).subs(sol) + Vv)
    lin_px = sp.simplify(sp.diff(Hm, px, 2)) == 0 and sp.diff(Hm, px) != 0
    P(f"  kinetic Hessian in (v, dPi/dt): {Hess.tolist()}, eigenvalues {ev}")
    P(f"  Hamiltonian H = {Hm}  (linear in p_x: {lin_px})")
    RES["numbers"]["H5"] = dict(eigs=[str(x) for x in ev], H=str(Hm), linear_in_px=bool(lin_px))
    P(f"  [{'FAIL' if lin_px else 'PASS'} for C2] H5: Hamiltonian linear in p_x => unbounded below (Ostrogradsky-type ghost); "
      "conditional on the recalled BLT form (PROVISIONAL). C1's dust kinetic term sigma v^2/2 alone: positive.")
    RES["checks"]["H5 C2 kinetic"] = dict(ok=not lin_px, detail="C2 Hamiltonian linear in p_x (ghost); C2 is not C1")

    # ============================================================== H6 L49 read literally with inertia rho_c
    P("\nH6  L49 with inertia rho_c = rhobar + div P (a real medium): L = |dP/dt|^2/(2 rho_c) - V[P]")
    rc, lam_v, kk, gm = sp.symbols("rho_c lambda_V k gamma", real=True)
    w2 = sp.simplify(rc * (lam_v + gm * kk ** 2))
    P(f"  omega^2 = {w2}  (lambda_V >= 0: the convex L49 potential's Hessian; gamma k^2 the stiffness)")
    sad = json.load(open(os.path.join(HERE, "ag6c_s0_saddle_results.json")))
    fid = sad["numbers"]["fiducials"]["F1_MW-M31_canonical"]
    fix = sad["numbers"]["fixed_point_convergence"]["0.2"][1]
    Kn = 4 * math.pi * 6.67430e-11
    rhoc_neg = fix * fid["unit_kg_m3"] + 2.2569e-27           # rho_c at R = 0.2 d in the F1 mid-plane (converged value)
    rate_L = math.sqrt(abs(rhoc_neg) * Kn / 2) * 2 * math.pi   # at k = 2 pi/L*, independent of L*
    P(f"  F1 mid-plane at R = 0.2 d: rho_c = rhobar + rho_ph = {rhoc_neg:.3e} kg/m^3 < 0 => omega^2 < 0, growth ~ k "
      f"(gradient instability); rate at k = 2 pi/L* = {rate_L:.2e} s^-1 (e-fold {1 / rate_L / 3.156e16:.2f} Gyr), "
      f"x(k L*/2pi) above")
    RES["numbers"]["H6"] = dict(rho_c=rhoc_neg, rate_at_2pi_over_Lstar=rate_L)

    # ============================================================== causality table
    P("\nCausality (reported): static backgrounds, max mode speed v_max = sqrt(1 + e) c (extraordinary, k perpendicular to E)")
    P("  criterion A (inside the light cone): FAILS for every e > 0 (forced: concave D(E) <=> convex W_rem)")
    ctab = {}
    for e in (1, 10, 1e2, 1e3, 1e4):
        row = []
        for vb in (300e3, 1000e3, 3000e3):
            m = math.sqrt(1 + e) * vb / 2.99792458e8
            ctab[f"e{e:g}_v{vb / 1e3:g}"] = m
            row.append(f"{m:.3f}")
        P(f"  e = {e:7g}: sqrt(1+e) v_bulk/c for v_bulk = 300/1000/3000 km/s: {' / '.join(row)}  (criterion B needs < 1)")
    RES["numbers"]["causality_B"] = ctab
    P("  all-frame ill-posedness line (H3c) for dark fields of non-relativistic cold currents, B' ~ (v/c) E':")
    P("  (v/c)^2 e^2 >= e sqrt(1 - (v/c)^2)  <=>  e >= sqrt(1 - b^2)/b^2 ~ (c/v)^2; for v = 300/1000/3000 km/s: e >= "
      + " / ".join(f"{math.sqrt(1 - (vv / 2.99792458e5) ** 2) / (vv / 2.99792458e5) ** 2:.1e}" for vv in (300, 1000, 3000))
      + " a0 (static galaxies scanned to e = 1e4)")

P(f"\nrun time {time.time() - T0:.1f} s")
RES["fails"] = FAILS
json.dump(RES, open(os.path.join(HERE, f"ag6c_gate_iv_results{SUF}.json"), "w"), indent=1, default=float)
P("FAILS:", FAILS if FAILS else "none")
OUT.close()
sys.exit(1 if FAILS else 0)
