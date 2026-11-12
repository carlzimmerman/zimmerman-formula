#!/usr/bin/env python3
"""CT14 H2: C'' on a static weak-field background, frozen coefficients, PN.
V3X's PN quadratic action for (delta Phi, delta sigma, delta P) (V3X README:81) + delta phi with W(P; a(rho_phi)), rho_phi = X + V.
Hermitian Fourier matrix in z = (phi, sigma, Phi, Px, Py, Pz); g along z, k at angle theta.
Criteria: FROZEN_CRITERIA.md (H2), written first. Units a0 (background) = c = K = 4 pi G = 1. mpmath for the roots (40 digits).
kappa = 1/2 FITTED; not theory closed. Grading only."""
import os, sys, math, time, json, resource, itertools
os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np
import sympy as sp
import mpmath as mp

T0 = time.time(); CH = []
def check(n, ok, note=""):
    CH.append(bool(ok)); print(f"  [{'PASS' if ok else 'FAIL'}] {n}" + (f"  ({note})" if note else ""), flush=True)

KAP = 0.5; EPS = KAP**2 / (8 * math.pi); RHO = 4 * math.pi / KAP**2        # rho_phi = a^2/(kappa^2 G), G = 1/4pi
print("=" * 100); print("CT14 H2: C'' static weak field, frozen coefficients (phi, khronon sigma, lapse Phi, covector P)"); print("=" * 100)

# ------------------------------------------------ W(P; a) and its derivatives (K = 1), symbolic
P_, a_, s_ = sp.symbols("P a s", positive=True)
W = a_ * (-P_ - a_ * sp.log(1 - P_ / a_))                     # W' = A = a P/(a - P): inverse of P = a mu(A/a), mu = s/(1+s)
check("S0 W'(P) = A(P) with P = a s/(1+s)", sp.simplify(sp.diff(W, P_).subs(P_, a_ * s_ / (1 + s_)) - a_ * s_) == 0)
hs = 2 * (s_ - sp.log(1 + s_)) - s_**2 / (1 + s_)
Pb = a_ * s_ / (1 + s_)
Wa = sp.diff(W, a_).subs(P_, Pb)
check("S1 -dW/da|_P = h(s) (so -W_rho = eps h: the a0-charge of law S, CT13 R1a)", sp.simplify(-Wa.subs(a_, 1) - hs.subs(a_, 1)) == 0)
exprs = {"HL": sp.diff(W, P_, 2), "HT": sp.diff(W, P_) / P_, "Wa": sp.diff(W, a_), "Waa": sp.diff(W, a_, 2), "WPa": sp.diff(W, P_, a_)}
num = {k_: sp.lambdify(s_, sp.simplify(v_.subs(P_, Pb).subs(a_, 1)), "mpmath") for k_, v_ in exprs.items()}
print(f"  H_L = {sp.factor(sp.simplify(exprs['HL'].subs(P_, Pb)))}, H_T = {sp.factor(sp.simplify(exprs['HT'].subs(P_, Pb)))}, "
      f"W_Pa = {sp.factor(sp.simplify(exprs['WPa'].subs(P_, Pb)))}, W_aa = {sp.factor(sp.simplify(exprs['Waa'].subs(P_, Pb)))}")

mp.mp.dps = 40
def build(s, th, opw, rt, gam, muK, k, cg=1, couple=True, qs=False):
    """Hermitian H(omega) = H0 + w H1 + w^2 H2 for z = (phi, sigma, Phi, Px, Py, Pz). L_avg = z^dag H z."""
    s = mp.mpf(s); k = mp.mpf(k)
    HL, HT = num["HL"](s), num["HT"](s)
    a_r = mp.mpf(1) / (2 * RHO); a_rr = -mp.mpf(1) / (4 * RHO**2)
    Wr = num["Wa"](s) * a_r; Wrr = num["Waa"](s) * a_r**2 + num["Wa"](s) * a_rr; WPr = num["WPa"](s) * a_r
    if not couple:
        Wr = Wrr = WPr = mp.mpf(0)
    v = mp.sqrt(opw * RHO); Hub = mp.sqrt(2 * RHO / (3 * mp.mpf("0.7"))); V1 = -3 * Hub * v; V2 = mp.mpf(0)
    if not couple:
        v = V1 = mp.mpf(0)
    kv = [k * mp.sin(th), mp.mpf(0), k * mp.cos(th)]
    n = 6; Hm = [[[mp.mpc(0)] * n for _ in range(n)] for _ in range(3)]          # Hm[p][i][j]: coefficient of w^p
    # symbols: time derivative -> (-i w) (power 1), grad_l -> i k_l (power 0)
    def add(c, i, d1, j, d2):
        """real term c (D1 f_i)(D2 f_j); d = list of (power of w, complex factor)."""
        for (p1, f1) in d1:
            for (p2, f2) in d2:
                # (d1 z_i)(d2 z_j)^* : w^p1 f1 * conj(w^p2 f2) = w^(p1+p2) f1 conj(f2) (w real)
                val = c * f1 * mp.conj(f2) / 4
                Hm[p1 + p2][j][i] += val
                Hm[p1 + p2][i][j] += mp.conj(val)
    one = [(0, mp.mpc(1))]; dt = [(1, mp.mpc(0, -1))]
    gr = lambda l: [(0, mp.mpc(0, 1) * kv[l])]
    divP = None
    PHI, SIG, PH, PX = 0, 1, 2, 3
    # T1 -|grad Phi|^2/2K
    for l in range(3): add(-mp.mpf(1) / 2, PH, gr(l), PH, gr(l))
    # T2 +grad(dXi1).dP, dXi1 = Phi - sigma_dot
    for l in range(3):
        add(mp.mpf(1), PH, gr(l), PX + l, one)
        if not qs:                                   # MUTATE qs: CT13's quasi-static khronon (sigma_dot left out of A)
            add(mp.mpf(-1), SIG, [(1, mp.mpc(0, -1) * mp.mpc(0, 1) * kv[l])], PX + l, one)
    # T3 -rho_tau |grad sigma|^2 / 2
    for l in range(3): add(-rt / 2, SIG, gr(l), SIG, gr(l))
    # T4 -dP.H.dP/2 (g along z: H = diag(HT, HT, HL))
    for l, hh in zip(range(3), [HT, HT, HL]): add(-hh / 2, PX + l, one, PX + l, one)
    # T5 -(gamma/2)(div dP)^2
    for l in range(3):
        for m in range(3): add(-gam / 2, PX + l, gr(l), PX + m, gr(m))
    # T6 (mu_K^2/2K) dXi1^2
    Xi = [(PH, one)] + ([] if qs else [(SIG, [(1, mp.mpc(1) * mp.mpc(0, 1))])])                      # -sigma_dot -> -(-i w) = +i w
    for (i, di) in Xi:
        for (j, dj) in Xi: add(muK**2 / 2, i, di, j, dj)
    # T7 phi own: phidot^2/2 - |grad phi|^2/2 - V'' phi^2/2
    add(mp.mpf(1) / 2, PHI, dt, PHI, dt)
    for l in range(3): add(-mp.mpf(1) / 2, PHI, gr(l), PHI, gr(l))
    add(-V2 / 2, PHI, one, PHI, one)
    # delta rho = v phidot + V' phi
    drho = [(1, -mp.mpc(0, 1) * v), (0, mp.mpc(V1))]
    # T8 -W_Prho (g.dP) drho
    add(-WPr, PX + 2, one, PHI, drho)
    # T9 -W_rhorho drho^2 / 2
    add(-Wrr / 2, PHI, drho, PHI, drho)
    # T10 -W_rho d2rho, d2rho = (phidot^2 - |grad phi|^2 + V'' phi^2)/2
    add(-Wr / 2, PHI, dt, PHI, dt)
    for l in range(3): add(Wr / 2, PHI, gr(l), PHI, gr(l))
    add(-Wr * V2 / 2, PHI, one, PHI, one)
    # T11 lapse coupling -Phi [(1 - W_rho... ) ]: -Phi[(1 + eps h) v phidot + (1 - eps h) V' phi], eps h = -W_rho
    epsh = -Wr
    add(-cg, PH, one, PHI, [(1, -mp.mpc(0, 1) * v * (1 + epsh)), (0, mp.mpc(V1 * (1 - epsh)))])
    return [mp.matrix(Hm[p]) for p in range(3)], dict(epsh=epsh, HL=HL, HT=HT)

def modes(Hs, dyn=(0, 1)):
    """roots of det(H0 + w H1 + w^2 H2) = 0 via elimination of the w-free constraint block, then a companion problem."""
    H0, H1, H2 = Hs
    n = H0.rows
    dyn = list(dyn)                                # phi, sigma carry time derivatives; Phi and P are constraints (no w in their block)
    con = [i for i in range(n) if i not in dyn and i != 1]
    def sub(M, r, c): return mp.matrix([[M[i, j] for j in c] for i in r])
    Cc = sub(H0, con, con); Ci = mp.inverse(Cc)
    assert all(abs(H1[i, j]) == 0 and abs(H2[i, j]) == 0 for i in con for j in con), 'constraint block must be w-free'
    # S(w) = Hdd(w) - Hdc(w) Hcc^-1 Hcd(w); Hdc has at most w^1 entries (sigma_dot - P)
    A0 = sub(H0, dyn, dyn) - sub(H0, dyn, con) * Ci * sub(H0, con, dyn)
    A1 = sub(H1, dyn, dyn) - sub(H1, dyn, con) * Ci * sub(H0, con, dyn) - sub(H0, dyn, con) * Ci * sub(H1, con, dyn)
    A2 = sub(H2, dyn, dyn) - sub(H1, dyn, con) * Ci * sub(H1, con, dyn)
    m = len(dyn)
    # companion: [0 I; -A2^-1 A0, -A2^-1 A1] x = w x
    A2i = mp.inverse(A2)
    Big = mp.zeros(2 * m, 2 * m)
    for i in range(m):
        Big[i, m + i] = 1
    T0_ = -A2i * A0; T1_ = -A2i * A1
    for i in range(m):
        for j in range(m):
            Big[m + i, j] = T0_[i, j]; Big[m + i, m + j] = T1_[i, j]
    ev, ER = mp.eig(Big)
    out = []
    for idx, w in enumerate(ev):
        z = mp.matrix([ER[i, idx] for i in range(m)])
        Mw = A0 + w * A1 + w**2 * A2
        dM = A1 + 2 * w * A2
        kre = (z.H * dM * z)[0] * w
        out.append((w, kre))
    return out, (A0, A1, A2, dyn)

# ------------------------------------------------ known answer: phi decoupled reproduces V3X's khronon dispersion
print("\nK1 known answer (phi decoupled, mu_K = 0): omega^2 = rho_tau [gamma k^2 + 1/(khat.H^-1.khat) - 1] (V3X README:128, H4)")
worst = mp.mpf(0)
for s in (0.1, 1.0, 10.0, 1e4):
    for th in (0.0, 0.7, math.pi / 2):
        for rt, gam, k in ((1.0, 0.0, 10.0), (1e-3, 1e5, 1e3)):
            Hs, info = build(s, th, 0.3, mp.mpf(rt), mp.mpf(gam), mp.mpf(0), k, couple=False)
            md, _ = modes(Hs)
            HL, HT = info["HL"], info["HT"]
            q = mp.sin(th)**2 / HT + mp.cos(th)**2 / HL
            w2pred = rt * (gam * k**2 + 1 / q - 1)
            w2s = sorted(set([mp.nstr(mp.re(w**2), 25) for w, _ in md]), key=lambda z: mp.mpf(z))
            dust = min((abs(mp.re(w**2) / w2pred - 1) for w, _ in md if abs(mp.re(w**2) - k**2) > 1e-6 * k**2), default=mp.mpf(1))
            worst = max(worst, dust)
check("K1 dust branch omega^2 matches V3X/H4 formula", worst < 1e-9, f"max rel {mp.nstr(worst, 3)}")

# ------------------------------------------------ analytic: kinetic determinant for k || g in the A representation
print("\nA1 analytic (A representation, gamma_L = 0): L_J(A, rho) with A = grad(Phi - sigma_dot); kinetic matrix of (phi, sigma) for k || g")
Aa, rr = sp.symbols("A rho", positive=True)
ss_ = sp.Symbol("s", positive=True)
a_of = sp.sqrt(sp.Rational(1, 4) * rr / (4 * sp.pi))          # a^2 = kappa^2 G rho, G = 1/4pi, kappa = 1/2
LJ = a_of**2 * (Aa / a_of - sp.log(1 + Aa / a_of))             # L_J = (a^2/K) f(A/a), K = 1
rb = 4 * sp.pi / sp.Rational(1, 4)                             # background rho_phi (a = 1)
LAA = sp.diff(LJ, Aa, 2); LAr = sp.diff(LJ, Aa, rr); Lrr = sp.diff(LJ, rr, 2); Lr = sp.diff(LJ, rr)
sub = {rr: rb, Aa: ss_}
opw_ = sp.Symbol("opw", positive=True)
epsh_s = sp.simplify(Lr.subs(sub))
Kt_free = sp.simplify(1 + epsh_s + Lrr.subs(sub) * opw_ * rb)
Kt_lock = sp.simplify(Kt_free - LAr.subs(sub)**2 * opw_ * rb / LAA.subs(sub))
hsym = 2 * (ss_ - sp.log(1 + ss_)) - ss_**2 / (1 + ss_)
epsS = sp.Rational(1, 4) / (8 * sp.pi)
check("A1a dL_J/drho = eps h(s)", sp.simplify(epsh_s - epsS * hsym) == 0)
check("A1b K_t(free P) = 1 + eps[h - (1+w) s h'/2] (CT13 R2b)", sp.simplify(Kt_free - 1 - epsS * (hsym - opw_ * ss_ * sp.diff(hsym, ss_) / 2)) == 0)
target = 1 + epsS * (hsym - opw_ * ss_**3 / (2 * (1 + ss_)))
check("A1c det K(phi, sigma) / (L_AA k^2) = K_t,eff = K_t(free) - L_Arho^2 v^2/L_AA = 1 + eps[h - (1+w) s^3/(2(1+s))] (= the fixed-P coefficient)",
      sp.simplify(Kt_lock - target) == 0)
print("  reason: delta A = grad(delta Phi - delta sigma_dot) contains the khronon velocity; the v phidot dependence of A's conjugate is absorbed by sigma,")
print("  leaving phi with the fixed-P coefficient. CT13's R2 treated delta g as a static constraint (+B^2/|L_gg|), which removes exactly this.")
Kl = sp.lambdify((ss_, opw_), target, "mpmath")
print("  threshold s*(1+w): K_t,eff = 0 (k || g); g* = s* a0 per footing; cone half-angle at 2 s*: tan^2 theta < |K_t,eff| / ((1+s) K_t,free)")
thr = {}
Kf_l = sp.lambdify((ss_, opw_), Kt_free, "mpmath")
for ow in (1e-5, 1e-4, 1e-3, 0.01, 0.05, 0.1, 0.3, 1.0):
    sst = mp.findroot(lambda z: Kl(mp.exp(z), ow), mp.log(4 / (EPS * ow)))
    sst = mp.exp(sst); thr[ow] = float(sst)
    s2 = 2 * sst; ang = mp.atan(mp.sqrt(-Kl(s2, ow) / ((1 + s2) * Kf_l(s2, ow))))
    print(f"    1+w {ow:7.0e}: s* = {mp.nstr(sst, 6):>10s}; g* = {float(sst)*9.3603e-11:.3e} (canonical) / {float(sst)*1.1312e-10:.3e} (alt) m/s^2; "
          f"unstable cone at 2 s*: theta < {float(ang)*180/math.pi:.2f} deg")

# ------------------------------------------------ mutation control: CT13's quasi-static khronon must PASS
print("\nM1 MUTATE (CT13's quasi-static khronon: sigma_dot left out of A, sigma not dynamical): s 108.9, 1e4, theta 0, 1+w 0.05 / 0.3")
mut_ok = True
for s in (108.9, 1e4):
    for ow in (0.05, 0.3):
        Hs, _ = build(s, 0.0, ow, mp.mpf(1e-6), mp.mpf(0), mp.mpf(0), 1e4, qs=True)
        md, (A0, A1, A2, dyn) = modes(Hs, dyn=(0,))
        okm = all(abs(mp.im(w**2)) <= 1e-20 * abs(w**2) and mp.re(w**2) > 0 for w, _ in md) and mp.re(A2[0, 0]) > 0
        Hs, _ = build(s, 0.0, ow, mp.mpf(1e-6), mp.mpf(0), mp.mpf(0), 1e4)
        md2, _ = modes(Hs)
        unst = max(abs(mp.im(w)) for w, _ in md2)
        mut_ok &= okm
        print(f"  s {s:g} 1+w {ow}: quasi-static K_t {mp.nstr(4*mp.re(A2[0,0]), 6)} (CT13 R2b {mp.nstr(Kf_l(s, ow), 6)}), stable {okm}; full: max |Im omega| / k = {mp.nstr(unst/1e4, 4)}")
check("M1 the quasi-static mutation reproduces CT13's pass (so the new result comes from sigma_dot in A)", mut_ok)

# ------------------------------------------------ the grid
S_LIST = [1e-3, 0.1, 1.0, 10.0, 108.9, 1e4, 1e8, 2.7e12]
TH = [i * math.pi / 12 for i in range(7)]
OPW = [1e-4, 0.05, 0.3, 1.0]
RT = [1e-6, 1.0, 1e3]
GAM = [0.0, 1e5]
MUK = [0.0, 0.1]
KS = [1e2, 1e4, 1e6]
print(f"\nH2 grid: s {S_LIST}, theta 7 values on [0, pi/2], 1+w {OPW}, rho_tau {RT}, gamma_L {GAM}, mu_K {MUK}, k {KS}; lapse coupling on/off")
bad_ghost = []; bad_inst = []; kin_bad = []; ks_min = mp.inf; kt_min = mp.inf; ncase = 0; worst_w2 = mp.inf
summ = {}
for s in S_LIST:
    smin_ks = mp.inf; smin_kt = mp.inf; smin_w2c2 = mp.inf; smin_kin = mp.inf; nb = 0
    for th, opw, rt, gam, muK, k, cg in itertools.product(TH, OPW, RT, GAM, MUK, KS, (1, 0)):
        if cg == 0 and not (rt == 1.0 and gam == 0.0 and muK == 0.0):
            continue
        ncase += 1
        Hs, info = build(s, th, opw, mp.mpf(rt), mp.mpf(gam), mp.mpf(muK), k, cg=cg)
        md, (A0, A1, A2, dyn) = modes(Hs)
        # kinetic matrix of (phi, sigma): A2 (coefficient of w^2) must be positive definite (L = z^dag (w^2 A2 + ...) z)
        ev2 = [mp.re(z) for z in mp.eighe(mp.matrix([[(A2[i, j] + mp.conj(A2[j, i])) / 2 for j in range(A2.cols)] for i in range(A2.rows)]), eigvals_only=True)]   # complex Hermitian
        kmin = min(ev2)
        smin_kin = min(smin_kin, kmin / max(ev2))
        if kmin <= 0: kin_bad.append((s, th, opw, rt, gam, muK, k, cg, mp.nstr(kmin, 5)))
        # effective phi coefficients: K_t = 4 A2_phiphi, K_s = -4 A0_phiphi/k^2 (mass terms subtracted)
        Hs2, _ = build(s, th, opw, mp.mpf(rt), mp.mpf(gam), mp.mpf(muK), 2 * k, cg=cg)
        _, (A0b, _, _, _) = modes(Hs2)
        Kt = 4 * mp.re(A2[0, 0]); Ks = -4 * mp.re(A0b[0, 0] - A0[0, 0]) / (3 * k**2)      # k^2 coefficient (mass terms cancel)
        smin_ks = min(smin_ks, Ks); smin_kt = min(smin_kt, Kt)
        for w, kre in md:
            w2 = w**2
            if abs(mp.im(w2)) > 1e-20 * (1 + abs(w2)) or mp.re(w2) < 0:
                # allow O(H) Hubble-scale rates (k-independent mass terms): flag only if |w|^2 > 1 (units a0/c, H ~ 9.8)
                if abs(w) > 30:
                    bad_inst.append((s, th, opw, rt, gam, muK, k, cg, mp.nstr(w, 6)))
                    nb += 1
            elif mp.re(w) > 0 and mp.re(kre) <= 0:
                bad_ghost.append((s, th, opw, rt, gam, muK, k, cg, mp.nstr(w, 6), mp.nstr(kre, 4)))
                nb += 1
            if mp.re(w2) > 0 and abs(mp.im(w2)) <= 1e-20 * abs(w2):
                smin_w2c2 = min(smin_w2c2, mp.re(w2))
    summ[s] = dict(min_Ks=mp.nstr(smin_ks, 8), min_Kt=mp.nstr(smin_kt, 8), min_kin_ratio=mp.nstr(smin_kin, 4), bad=nb)
    ks_min = min(ks_min, smin_ks); kt_min = min(kt_min, smin_kt)
    h_ = 2 * (s - math.log1p(s)) - s * s / (1 + s) if s > 1e-2 else s**3 / 3 - s**4 / 2
    print(f"  s {s:9.3g}: own K_s 1+eps h = {1 + EPS*h_:.6g}; effective min K_s {mp.nstr(smin_ks, 8)}, min K_t {mp.nstr(smin_kt, 8)}; "
          f"kinetic matrix (phi, sigma) min eig/max eig {mp.nstr(smin_kin, 3)}; ghosts/instabilities {nb}  ({time.time()-T0:.0f}s)", flush=True)
print(f"  cases {ncase}")
check("H2 no ghost: every real root has positive Krein energy", not bad_ghost, f"{len(bad_ghost)} bad; first {bad_ghost[:2]}")
check("H2 no gradient instability: no complex/negative omega^2 beyond the Hubble-scale mass terms (|omega| > 30 a0/c)", not bad_inst, f"{len(bad_inst)} bad; first {bad_inst[:2]}")
check("H2 constrained kinetic matrix of (phi, sigma) positive definite", not kin_bad, f"{len(kin_bad)} bad; first {kin_bad[:2]}")
check("H2 effective phi gradient coefficient >= 1 (no CT7 flip from P, stiffness, dust, lapse)", ks_min >= 1 - 1e-12, f"min {mp.nstr(ks_min, 10)}")
json.dump({"per_s": {str(k_): v_ for k_, v_ in summ.items()}, "cases": ncase, "ghost": [list(map(str, b)) for b in bad_ghost[:20]],
           "inst": [list(map(str, b)) for b in bad_inst[:20]], "kin_bad": [list(map(str, b)) for b in kin_bad[:20]],
           "min_Ks": str(ks_min), "min_Kt": str(kt_min)}, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ct14_h2_static.json"), "w"), indent=1)
print(f"\nchecks {sum(CH)}/{len(CH)}; peak RSS {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1e9:.2f} GB; {time.time()-T0:.0f}s")
print("kappa = 1/2 FITTED; not theory closed.")
